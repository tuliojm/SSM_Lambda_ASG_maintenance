# SSM_Lambda_ASG_maintenance
AWS Systems Manager Automation command to put/remove instance in a AutoScaling Group in standby.

## Objectives:
- Put instances in an AutoScaling group in standby before running maintenance tasks.
- Bring them back to work after the maintenance. 

## Howto

### Creating the Automation Document:
- In the Systems Manager's dashboard, click on Documents (left menu).
- Click "Create Document."
- Specify a name (Ex: AutomationChangeASGState).
- In "Documet type," select Automation.
- In Content, paste the content of the file AutomationChangeASGState.json.

### Creating the Lambda function:
- On the Lambda dashboard, click on "Create Function."
- Select "Author From Scratch."
- Specify the following options:
 - Name: asg-state-change-lambda
 - Runtime: select "Python 2.7"
 - Role: select "Choose an existing one"
 - Existing Role: yourRole
- Click create
- Scroll the down until the "Function Code" section.
- In "Code entry type," select "Edit code inline."
- Paste the contents of lambda_function.py 
- In the "Basic settings," change the Timeout to 10 seconds.
- Click save

### IAM role with the following trust relationship:
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com",
        "Service": "ssm.amazonaws.com",
        "Service": "lambda.amazonaws.com"

      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
and the following example policies (restrict according to your needs):
- AmazonEC2FullAccess
- AWSLambdaFullAccess
- AmazonEC2RoleforSSM
- AmazonSSMAutomationRole
- AmazonSSMMaintenanceWindowRole
- AutoScalingFullAccess

### Adittional requirements:
- Configure the AutoScaling Group's Launch Configuration.
- Create the Systems Manager's patch baseline.
- Create the Systems Manager's Patch Groups
- Associate the Patch Baseline with the Patch Group.
- Create the Maintenance Window with the following input Parameters:
 - AutoScalingGroupName: (The Auto Scaling Group name)
 - DesiredState: [Standby|Active] (Case sensitive, choose either Standby or Active)
 - PatchGroupValue: managed instances patch group 
 - AutomationAssumeRole: (the ARN for the IAM role. EX: arn:aws:iam::XXXXXXXXXXXX:role/myrole)
