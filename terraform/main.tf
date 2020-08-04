module "dispatch" {
  source       = "git@gitlab.internal.unity3d.com:sre/sre-service-tf-module"
  service_name = local.service_name
  iam          = {
    roles = [
      "roles/iam.workloadIdentityUser",
    ]
  }

  dns = [
    {
      name              = local.service_name,
      managed_zone_name = "test-sre-ie-internal-unity3d-com",
      managed_zone_dns  = "test.sre.ie.internal.unity3d-com"
    }
  ]

  pubsub = {
    subscriptions = [
      local.alert_events_topic_name,
      local.incident_events_topic_name,
    ]

    publishes_to = [
      local.health_status_change_events_topic_name
    ]
  }
}