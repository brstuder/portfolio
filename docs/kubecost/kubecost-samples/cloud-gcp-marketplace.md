# Kubecost Cloud GCP Marketplace Licensing

!!! info "Author's Note"
    
    This example is a very simple installation guide which takes users through the GCP Marketplace to purchase and install the Kubecost dashboard. Currently, Kubecost is no longer available through the GCP Marketplace, so you will not be able to recreate these steps firsthand.

Kubecost Cloud is [available for licensing on GCP Marketplace](https://console.cloud.google.com/marketplace/product/kubecost-public/kubecost-cloud) and can be installed in minutes. This guide will take you through licensing through GCP Marketplace, and next steps for setting up Kubecost Cloud. Kubecost currently offers 30 days of Kubecost Cloud free without licensing fees.

!!! note

    Licensing Kubecost Cloud through GCP Marketplace will not directly integrate your GCP billing data into your Kubecost Cloud environment. For more information, see our GCP Cloud Integration guide.

### Prerequisites

* Set up a Google Cloud account with an attached [billing account](https://cloud.google.com/billing/docs/how-to/create-billing-account).
* Set up a Kubecost Cloud account

### GCP Marketplace licensing guide

On the [Product details page for Kubecost](https://console.cloud.google.com/marketplace/product/kubecost-public/kubecost-cloud), select *Subscribe*. You will be taken to an Order Summary page.

![image](../../images/kubecost/gcp1.png)

Under "1. Select Plan", the default plan should be Cloud Pro, and the default usage fee should be USD 0.167 per node per day. You can use the Pricing Calculator in the right sidebar to determine estimated costs by providing estimated timeframe of usage from 1 day to 1 year, and total node count.

![image](../../images/kubecost/gcp2.png)

Under "2. Purchase Details", select the billing account you wish to associate Kubecost Cloud with from the dropdown.

Under "3. Terms", read and agree to the terms and conditions, which include Google Cloud Marketplace Terms of Service as well as the Kubecost Terms of Service. Then, select *Subscribe*. Wait a moment while your order request is processed. Select *Go to Product Page* in the pop-up which should appear once the order has been sent to Kubecost. If you have not already, select *Sign up with provider* on the product page and provide all necessary user info to get your Kubecost Cloud account set up. Purchase orders should be automatically processed. Refresh the product page until you see *Manage on Provider*. Selecting this will take you from GCP Marketplace to the Kubecost Cloud login page.

![image](../../images/kubecost/gcp3.png)

You should now have access to the Kubecost Cloud dashboard.

### Next steps

After having licensed Kubecost Cloud, you are able to install the Kubecost Cloud Agent onto all clusters you want to receive cost metrics for. See our existing Installation and Onboarding guide for help getting started.