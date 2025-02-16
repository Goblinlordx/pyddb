resource "aws_dynamodb_table" "main" {
    name = "test-tx-st"
    hash_key         = "PK"
    range_key        = "SK"
    billing_mode     = "PAY_PER_REQUEST"

    attribute {
        name = "PK"
        type = "S"
    }

    attribute {
        name = "SK"
        type = "S"
    }

    attribute {
        name = "GSI1PK"
        type = "S"
    }

    attribute {
        name = "GSI1SK"
        type = "S"
    }

    attribute {
        name = "GSI2PK"
        type = "S"
    }

    attribute {
        name = "GSI2SK"
        type = "S"
    }

    attribute {
        name = "GSI3PK"
        type = "S"
    }

    attribute {
        name = "GSI3SK"
        type = "S"
    }

    attribute {
        name = "GSI4PK"
        type = "S"
    }

    attribute {
        name = "GSI4SK"
        type = "S"
    }

    global_secondary_index {
        name               = "GSI1"
        hash_key           = "GSI1PK"
        range_key          = "GSI1SK"
        projection_type    = "ALL"
    }
   
    global_secondary_index {
        name               = "GSI2"
        hash_key           = "GSI2PK"
        range_key          = "GSI2SK"
        projection_type    = "ALL"
    }
    
    global_secondary_index {
        name               = "GSI3"
        hash_key           = "GSI3PK"
        range_key          = "GSI3SK"
        projection_type    = "ALL"
    }
    
    global_secondary_index {
        name               = "GSI4"
        hash_key           = "GSI4PK"
        range_key          = "GSI4SK"
        projection_type    = "ALL"
    }
     

}