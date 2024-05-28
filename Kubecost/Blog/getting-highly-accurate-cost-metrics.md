> Author's Note: The original article can be found at https://blog.kubecost.com/blog/enhancing-cost-accuracy/

# Getting Highly Accurate and Granular Cost Metrics with Kubecost

In the world of cost monitoring and visibility, having accurate data is vital for businesses. When it comes to managing budgets, avoiding overspending, or enhancing efficiency, getting the most accurate information at your disposal makes all the difference. Kubecost offers several methods to enhance the accuracy of your Kubecost cost metrics. In this blog we explore each method, including the newest method for predicting short-term costs, before they are billed by their cloud service providers (CSPs).

## Harnessing cloud provider on-demand pricing

Without any configuration, Kubecost identifies the cloud service provider (CSP) source of clusters it has been installed on, and can then use public APIs from those CSPs to provide a starting point for its cost metrics. For AWS, this pricing is sourced from their [Price List Query API](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-price-list-query-api.html). For Azure, users must enable this pricing query through [configuration of the Billing Rate Card API](https://docs.kubecost.com/install-and-configure/install/cloud-integration/azure-out-of-cluster/azure-config).

This initial step serves as a passive, and directionally accurate, foundation for delivering cost insights. However, users can enhance data accuracy by taking additional measures.

## Cloud provider billing integration

Upon Kubecost installation, [integrating billing data with CSPs](https://docs.kubecost.com/install-and-configure/install/cloud-integration) should be a top priority. This will provide value beyond basic assets tracking, including any cloud services you use beyond just Kubernetes resources. Kubecost provides dedicated integration guides for all three major CSPs as well as additional troubleshooting and support.

![Example cloud integrations](/Kubecost/Blog/blog-images/cloudintegrations.png)

## Reconciliation

What’s crucial about cloud integration is that it will enable Kubecost to perform reconciliation, a process that matches in-cluster assets with items found in the billing data pulled from each CSP. This can correct the price, for example, of nodes prices that were previously assumed to be on-demand rates.

Kubecost’s Allocation and Assets pages have visual support for recognizing unreconciled costs. In the Kubecost UI, select Settings from the left navigation, then under ‘Pricing’, toggle on *Highlight Unreconciled Costs*, then select *Save* at the bottom of the page. Your most recent cost data will now be displayed with a hatching effect to distinguish it from reconciled data.

![Unreconciled costs](/Kubecost/Blog/blog-images/unreconciledcosts.png)

Reconciliation requires approximately 36-48 hours following resource usage to update accordingly.

## Short-term cost estimation

After completing reconciliation, Kubecost can then estimate node pricing for the period of time before the billing data is available. This estimation is used on hourly and daily intervals by comparing the past 7 days of actual billed costs.

## Catering to air-gapped environments

For users who don’t rely largely on CSP infrastructure, you may wonder what pricing features exist for you. Kubecost doesn’t forget about users with air-gapped environments, and makes sure to provide pricing assistance via custom and CSV pricing.

## Custom pricing

Kubecost provides a configurable pricing tool known as Custom Pricing, which can be adjusted through the product UI or your values.yaml file. Custom pricing allows you to provide manual monthly pricing values which will override cloud billing data from any APIs, which should be applied before any discounts. This includes values for CPU/GPU/RAM prices, as well as Spot CPU/RAM prices and storage prices.

![Custom pricing](/Kubecost/Blog/blog-images/custompricing.png)

To access custom pricing via the Kubecost UI, select the *Settings* page from the left navigation, then under ‘Pricing’, toggle on *Enable Custom Pricing*. You can adjust the fields as needed (just remember to select *Save* at the bottom of the page when finished). You can configure these values in your *values.yaml* file under the `kubecostProductConfigs` flag:

```
kubecostProductConfigs:
  customPricesEnabled: true
  defaultModelPricing:
    enabled: true
    CPU: 28.0 # Single core per month cost
    spotCPU: 4.86 # Single core per month cost
    RAM: 3.09 # GB per month cost
    spotRAM: 0.65 # GB per month cost
    GPU: 693.50 # per month cost
    spotGPU: 225.0 # per month cost
    storage: 0.04 # per GB per month cost
    zoneNetworkEgress: 0.01 # per GB per month cost
    regionNetworkEgress: 0.01 # per GB per month cost
    internetNetworkEgress: 0.12 # per GB per month cost
```

Once you’ve made your changes, run a `helm upgrade` command to your Kubecost environment:

```
$ helm upgrade kubecost cost-analyzer \
    --repo https://kubecost.github.io/cost-analyzer/ \
    --namespace kubecost --create-namespace \
    --values values.yaml
```

## CSV pricing

CSV pricing is an Enterprise-only (mature beta) feature which allows for further configuration of custom pricing. Using a CSV file, users can provide pricing information for individual assets such as on-prem clusters, or for external enterprise discounts. A complete summary for creating and configuring this CSV file can be found in our [CSV Pricing doc](https://docs.kubecost.com/install-and-configure/advanced-configuration/csv-pricing).

## Closing thoughts

Kubecost stands as the premier solution for Kubernetes and cloud service cost monitoring, providing unparalleled accuracy and granularity in cost insights. Whether you’re a cloud consumer or operating in air-gapped environments, Kubecost offers tailored features to provide you with the most up-to-date cost insights. If you haven’t used Kubecost before, you can [get started today in minutes](https://www.kubecost.com/install.html#show-instructions).