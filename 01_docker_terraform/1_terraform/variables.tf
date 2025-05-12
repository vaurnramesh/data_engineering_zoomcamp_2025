variable "credentials" {
  description = "My Credentials"
  default     = "~/.gc/google_credentials.json"
}


variable "project" {
  description = "Project"
  default     = "de-zoomcamp-00"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "australia-southeast1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "australia-southeast1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "trips_data_all"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "de-zoomcamp-00-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}