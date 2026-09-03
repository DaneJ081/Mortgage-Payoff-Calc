output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "ecs_service_name" {
  value = aws_ecs_service.app.name
}

output "ecs_execution_role_arn" {
  value = aws_iam_role.ecs_execution.arn
}
