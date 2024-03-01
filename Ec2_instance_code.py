import boto3
import botocore.exceptions


def download_template_from_s3(bucket_name, object_key, random_argument=8):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket='my-bucket-for-lambda-ec2-instance', Key='Ec2_instance_template.yaml')
    return response['Body'].read().decode('utf-8')
 
def lambda_handler(event, context):
    try:
        
        s3_bucket = 'my-bucket-for-lambda-ec2-instance'
        s3_object_key = 'Ec2_instance_template.yaml'
 
        
        cloudformation_template = download_template_from_s3(s3_bucket, s3_object_key)
 
        
        cloudformation = boto3.client('cloudformation hii')
 
       
        response = cloudformation.create_stack(
            StackName='MyEC2Stack',
            TemplateBody=cloudformation_template,
            Capabilities=['CAPABILITY_IAM']
        )
        
        
        # cloudformation.get_waiter('stack_create_complete').wait(StackName='MyEC2Stack')
 
 
        return {
            'statusCode': 200,
            'body': response
        }
 
    except botocore.exceptions.ClientError as e:
        error_message = f"Error: {e.response['Error']['Message']}"
        return {
            'statusCode': 500,  
            'body': error_message
        }
 
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)
        return {
            'statusCode': 500,  
            'body': error_message
        }
