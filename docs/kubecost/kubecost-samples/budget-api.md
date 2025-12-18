# Budget API

!!! info "Author's Note"

    The Kubecost Budget API allows organizations to establish spend rules across their operations. I chose to include this article in my portfolio as an API reference doc which presents a fairly straightforward way of setting up budget rules, including use cases and examples to demonstrate the API's intended use and limitations.

The Budget API allows you to create, update, and delete recurring budget rules to control your Kubernetes spending. Weekly and monthly budgets can be established on workloads to set limits on cost spend, with the option to configure alerts for reaching specified budget thresholds via email, Slack, or Microsoft Teams.

### Budget API

`POST` `http://<your-kubecost-address>/model/budget`

Creates a recurring budget rule or updates a recurring budget rule when provided the ID of the existing rule.

**Request Body**

| Name         | Type   | Description |
| ------------ | ------ | ----------- |
| name*        | string | Name of the budget rule |
| type*        | string | Budget type. Accepts `allocations`, `asset`, `cloud` or `collections` |
| values*      | map    | Used for specifying the workload category and name(s) for which the budget rule is applied, as key-value pairs. Keys represent the workload category; each value is a list of one or more names. |
| interval*    | string | The interval that the budget will reset with (either `weekly` or `monthly`). |
| intervalDay  | int    | The day the budget will reset. For `weekly`, `intervalDay=0` is Sunday, `1` is Monday, etc. For `monthly`, it corresponds to the day of the month. |
| spendLimit*  | int    | The budget limit value. |
| id           | string | Only used when updating a budget rule; the ID of the rule being modified. For more info, see the [Using the `id` parameter](#using-the-id-parameter) section below. |
| action       | string | Optional configurations for visibility when your budget exceeds a threshold. Can generate email or Slack/Teams messages. See the [Using Budget Actions](#using-budget-actions) section below. |


```py title="200: OK"
{
    "code": 200,
    "data":
        {
            "name": "<budget name>",
            "type": "<budget type>",
            "id": "<budget id>",
            "values": {
                "<category1>": [
                    "<name1>"
                ]
            },
            "kind": "",
            "interval": "",
            "intervalDay": ,
            "spendLimit": ,
            "actions": [
                {
                    "amount": 0,
                    "percentage": 1,
                    "slackWebhooks": [],
                    "msTeamsWebhooks": [],
                    "emails": [],
                    "lastFired": ""
                }
            ],
            "window": {
                "start": "",
                "end": ""
            },
            "currentSpend":
        }
}
```

### Get recurring budget rule(s) <a href="#get-recurring-budget-rule-s" id="get-recurring-budget-rule-s"></a>

`GET` `http://<your-kubecost-address>/model/budgets`

Lists all existing recurring budget rules

```py title="200: OK"
{
    "code": 200,
    "data":
        {
            "name": "<budget name>",
            "type": "<budget type>",
            "id": "<budget id>",
            "values": {
                "<category1>": [
                    "<name1>"
                ]
            },
            "kind": "",
            "interval": "",
            "intervalDay": "",
            "spendLimit": "",
            "actions": [
                {
                    "percentage": 1,
                    "slackWebhooks": [],
                    "msTeamsWebhooks": [],
                    "emails": [],
                    "lastFired": ""
                }
            ],
            "window": {
                "start": "",
                "end": ""
            },
            "currentSpend": 0.0
        }
}
```

### Delete recurring budget rule <a href="#delete-recurring-budget-rule" id="delete-recurring-budget-rule"></a>

`DELETE` `https://<your-kubecost-address>/model/deleteBudget`

Deletes a budget rule defined by `id`

**Path Parameters**

| Name | Type   | Description                                   |
| ---- | ------ | --------------------------------------------- |
| id\* | string | ID of the recurring budget rule to be deleted |

```py title="200: OK"
{
    "code": 200,
    "data": []
}
```

### Formatting parameters when creating/updating budget rules <a href="#formatting-parameters-when-creating-updating-budget-rules" id="formatting-parameters-when-creating-updating-budget-rules"></a>

Creating and updating recurring budget rules uses POST requests, which will require submitting a JSON object in the body of your request instead of adding parameters directly into the path (such as when deleting a recurring budget rule). See the [Examples](#examples) section below for more information on formatting your requests.

### Using the `id` parameter <a href="#using-the-id-parameter" id="using-the-id-parameter"></a>

The `id` parameter when using the endpoint `/budget` is considered optional, but its use will vary depending on whether you want to create or update a budget rule.

When creating a new budget rule, `id` should not be used. An ID for the budget rule will then be randomly generated in the response. When updating an existing budget rule, `id` needs to be used to identify which budget rule you want to modify, even if you only have one existing rule.

The `id` value of your recurring budget is needed to update or delete it. If you don't have the `id` value saved, you can retrieve it using `/budgets`, which will generate all existing budgets and their respective `id` values.

### Using Budget Actions <a href="#using-budget-actions" id="using-budget-actions"></a>

You can configure greater visibility towards tracking your budgets using the `actions` parameter, which will allow you to create alerts for when your budget spend has passed a specified percentage threshold, and send those alerts to you or your team via email, Slack, or Microsoft Teams.

When providing values for `actions`, `percentage` refers to the percentage of `spendLimit` which will result in an alert. For example, if `"spendLimit": 2000` is configured for a weekly budget rule and `"percentage": 50` is configured, an alert will be sent to all listed emails/webhooks if spending surpasses $1000 USD for the week.

```
"actions" : [
            {
                "percentage": 100,
                "slackWebhooks": [
                    "<example Slack webhook>"
                ],
                "emails": [
                    "foo@kubecost.com",
                    "bar@kubecost.com"
                ],
                "msTeamsWebhooks": [
                    "<example Teams webhook>"
                ]
            }
        ]
```

### Configuring currency <a href="#configuring-currency" id="configuring-currency"></a>

Kubecost supports configuration of the following currency types: USD, AUD, BRL, CAD, CHF, CNY, DKK, EUR, GBP, IDR, INR, JPY, NOK, PLN, and SEK. Kubecost does *not* perform any currency conversion when switching currency types; it is for display purposes, therefore you should ideally match your currency type to the type in your original cloud bill(s).

Currency type can only be changed via a `helm` upgrade to your *values.yaml*, using the flag `.Values.kubecostProductConfigs.currencyCode`. For example, if you needed to convert your currency type to EUR, you would modify the helm flag as:

```
kubecostProductConfigs:
    currencyCode: EUR
```

### Examples <a href="#examples" id="examples"></a>

**Create a recurring budget rule for my test cluster which resets every Wednesday with a budget of $100.00 USD, and will send an alert via email when spending has exceeded 75% of the spend limit.**

```
curl --location '<your-kubecost-address>/model/budget' \
--header 'Content-Type: application/json' \
--data-raw '{
        "name": "budget-rule",
        "type": "allocations",
        "values": {
            "cluster":["test"]
        },
        "kind": "soft",
        "interval": "weekly",
        "intervalDay": 3,
        "spendLimit": 100,
        "actions" : [
            {
                "percentage": 75,
                "emails": [
                    "foo@kubecost.com",
                ]
            }
        ]
}'
```

**Create a recurring budget rule for my `kubecost` namespace which resets on the 1st of every month with a budget of $400.00 USD, and will send an alert via Slack and Microsoft Teams when spending has exceeded $100.00 of the spend limit.**

```
curl --location '<your-kubecost-address>/model/budget' \
--header 'Content-Type: application/json' \
--data-raw '{
        "name": "budget-rule-2",
        "type": "allocations",
        "values": {
            "namespace":["kubecost"]
        },
        "kind": "soft",
        "interval": "monthly",
        "intervalDay": 1,
        "spendLimit": 400,
        "actions" : [
             {
                "percentage": 25,
                "slackWebhooks": [
                    "<example Slack webhook>"
                ],
                "msTeamsWebhooks": [
                    "<example Teams webhook>"
                ]
            }
        ]
}'
```