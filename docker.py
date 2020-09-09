import boto3
import json


def get_instance_info():
    instances = []
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # This sample print will output entire Dictionary object
            instance_info = (instance.name, instance, type)
            instances.append(instance_info)


def get_total_instance_cost(ec2_infos):
    prices = []
    for ec2 in ec2_infos:
        client = boto3.client('pricing')
        response = client.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {
                    'Type': ec2.type,
                    'region': 'us-west',
                    'os': "linux",
                    'Field': 'operation',
                    'Value': 'RunInstance'
                },
                ...
            ],
        )
        price_list = response["PriceList"]  # “unstructured” JSON
        price_item = json.loads(price_list[0])

        terms = price_item["terms"]
        term = terms["OnDemand"].itervalues().next()

        price_dimension = term["priceDimensions"].itervalues().next()
        price = price_dimension['pricePerUnit']["USD"]

        price.append(price)

    return sum(prices)


if __name__ == "__main__":
    instance_infos = get_instance_info()
    tot_cost = get_total_instance_cost(instance_infos)
    print(instance_infos)
    print('total cost of running ec2s is: ', tot_cost)
