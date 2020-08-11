#!/usr/bin/env bash

# CONSTANTS
APP=${PWD##*/}
GREEN="\033[0;38;5;2m"
YELLOW="\033[0;38;5;11m"
RED="\033[0;38;5;9m"
COLOR_OFF="\033[0m"
DONE="${GREEN}DONE!${COLOR_OFF}\n"
SUCCESS="SUCCESS!\n"
ERROR_MSG="${RED}ERROR: %s ${COLOR_OFF}\n"
FAIL_ON_ERROR=1
SKIP_ERROR=0
OUT_DIR=${PWD}/deploy
CHART_DIR=${OUT_DIR}/${APP}
[[ -v DIRTY ]] && ALLOW_DIRTY="--allow-dirty" || ALLOW_DIRTY=""

# CLI args
RELEASE_TYPE=${1}
TARGET=${2}
NO_CLEANUP=${3}

print_error() {
    echo -e "${RED}ERROR: $(head -n 1 /tmp/build)${COLOR_OFF}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $(head -n 1 /tmp/build)${COLOR_OFF}"
}

check_error() {
    exit_code=$1
    should_exit=$2
    if [[ ${exit_code} -ne 0 ]]; then
        if [[ ${should_exit} -ne 0 ]]; then
            print_error
            exit 1
        else
            print_warning
        fi
    else
        printf ${DONE}
    fi
}

get_version_info() {
    part=${1}
    set -e
    if [[  "${part}" == "rebuild" ]]; then
        current_version=$(.venv/bin/bumpv current)
        printf '{"current_version": "%s", "new_version": "%s"}' ${current_version} ${current_version}
    else
        .venv/bin/bumpv bump ${part} ${ALLOW_DIRTY} -o json
    fi
    set +e
}

build_image() {
    tag=$1
    printf "Building image with tag ${tag}..."
    docker build -t ${tag} --squash .
    check_error ${?} ${FAIL_ON_ERROR}
    printf "Pushing image with tag ${tag}..."
    docker push ${tag} &> /tmp/build
    check_error ${?} ${FAIL_ON_ERROR}
}

cleanup() {
    image=${1}
    previous_version=${2}
    if [[ "${3}" == "" ]]; then
        printf "Deleting previous image ${image}:${previous_version}..."
        docker rmi $( docker images | grep ${image} | grep ${previous_version} |  awk '{ print $3}' ) &> /tmp/build
        check_error ${?} ${SKIP_ERROR}
        printf "Removing previous Helm chart ${APP}/${previous_version}..."
        curl -s --request DELETE ${CHARTS_MUSEUM}/${APP}/${previous_version} &> /tmp/build
        check_error ${?} ${SKIP_ERROR}
    fi
}

package() {
    version=$1
    app=$2
    rm ${OUT_DIR}/*.tgz &> /tmp/build
    printf "Creating Helm chart ${app}:${version}..."
    helm package --version ${version} ${CHART_DIR} -d ${OUT_DIR} &> /tmp/build
    check_error ${?} ${FAIL_ON_ERROR}
}

update_helm_repo(){
    app=${1}
    version=${2}
    repo_url=${3}
    printf "Uploading Helm chart to ${repo_url#*@}/${app}:${version}..."
    curl -s --data-binary "@${OUT_DIR}/${app}-${version}.tgz" ${repo_url} &> /tmp/build
    check_error ${?} ${FAIL_ON_ERROR}
    printf "Updating Helm index file..."
    helm repo index ${CHART_DIR} --url ${repo_url} &> /tmp/build
    check_error ${?} ${SKIP_ERROR}
    printf "Updating Helm chart repos..."
    helm repo update &> /tmp/build
    check_error ${?} ${SKIP_ERROR}
}

# Version variables
set -e
version_info=$(get_version_info ${RELEASE_TYPE})
VERSION=$(echo ${version_info} | jq '.new_version' | tr -d \")
PREVIOUS_VERSION=$(echo ${version_info} | jq '.current_version' | tr -d \")
set +e

# Docker variables
PROJECT=unity-ie-sre-isolated-${TARGET}
DOCKER_REPO=gcr.io/${PROJECT}
IMAGE="${DOCKER_REPO}/${APP}"
DOCKER_TAG="${DOCKER_REPO}/${APP}:${VERSION}"

# Helm variables
REPO_URL=$( helm repo list | grep ${TARGET} |awk '{print $2}' )
CHARTS_MUSEUM=${REPO_URL}/api/charts

cleanup ${IMAGE} ${PREVIOUS_VERSION} ${NO_CLEANUP}
build_image ${DOCKER_TAG}
package ${VERSION} ${APP}
update_helm_repo ${APP} ${VERSION} ${CHARTS_MUSEUM}
