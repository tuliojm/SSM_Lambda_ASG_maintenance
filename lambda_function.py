import boto3


def getInstances(asg):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])
    instances = []

    if not response['AutoScalingGroups']:
        print('AutoScaling Group not found. Full response:\n %s' % str(response))
        return instances
    else:
        for instance in response.get('AutoScalingGroups')[0]['Instances']:
            instances.append(instance['InstanceId'])
        print('Instances list: %s' % str(instances))
        return instances

def checkTag(instance,tag,value):
    client = boto3.client('ec2')
    result=False
    response = client.describe_instances(InstanceIds=[instance])
    for i in response['Reservations'][0]['Instances'][0]['Tags']:
        print('Checking instance %s for tag %s : %s' % (instance, tag, value))
        if i['Key'] == tag:
            if i['Value'] == value:
                print('Found instance %s in Patch Group %s' % (str(response['Reservations'][0]['Instances'][0]['InstanceId']), value))
                result=True
            else: 
                print ('Could not find tag for instance %s' % instance)
    return result

def setInstanceStandby(asg,instances):
    client = boto3.client('autoscaling')
    print('Setting instances in standby: %s' % str(instances))
    response = client.enter_standby(InstanceIds=instances,AutoScalingGroupName=asg,ShouldDecrementDesiredCapacity=True) 

def setInstanceActive(asg,instances):
    client = boto3.client('autoscaling')
    print('Setting instances active: %s' % str(instances))
    response = client.exit_standby(InstanceIds=instances,AutoScalingGroupName=asg) 

def lambda_handler(event, context):
    print('Full Event: %s' % str(event))
    asg=event['AutoScalingGroupName']
    patchGroup=event['PatchGroupValue']
    desiredState=event['State']
    instances = getInstances(asg)
    InstancesList = []
    for instance in instances:
        if checkTag(instance,'Patch Group',patchGroup):
            print('Adding the instance %s in the list' % instance)
            InstancesList.append(instance)
                    
	
    if len(InstancesList) > 0:
        if desiredState == 'Standby':
            setInstanceStandby(asg,InstancesList)
        elif desiredState == 'Active':
            setInstanceActive(asg,InstancesList)
        else:
            print('Invalid state: %s' % desiredState)
            return False
        return True
	    

