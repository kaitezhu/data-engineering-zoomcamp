terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.25.0"
    }
  }
}

provider "google" {
  project = "xenon-depth-420805"
  region  = "australia-southeast2-a"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "xenon-depth-420805-terra-bucket"
  location      = "AUSTRALIA-SOUTHEAST2"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}