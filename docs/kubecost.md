# Kubecost

**Technical Writer, *June 2022 - June 2024***

| Criteria | Description |
|---|---|
| Documentation | GitHub, GitBook, Docusaurus, SnagIt, Markdown |
| Subject matter/industry | SaaS, Kubernetes, cloud services and billing |
| Points of contact | Solutions engineers, full-stack engineers, product managers |
| Target audience | Software developers, developer advocates, solutions engineers, and IT/governance and compliance personnel |

Kubecost (*KOOB*-cost) is a SaaS startup focused on providing cost visibility for cloud service spend in the Kubernetes space, and was acquired by IBM in 2024. For two years, I served as the company's first and only technical writer, as well as the primary maintainer of the company's documentation repository.

I have also contributed to company blog posts, release notes, API docs, and architecture diagrams. This collection of articles from my time there showcase the [Diataxis framework](https://idratherbewriting.com/blog/what-is-diataxis-documentation-framework) with articles which represent each of the four key content types. In this folder, you can see writing samples which include API documentation, install guides, custom software configurations, and Kubernetes concepts.

You can also see architecture diagrams [here](samples/diagrams.md), created with draw.io.

## Key Projects and Responsibilities

I oversaw our live docs site, [docs.kubecost.com](https://docs.kubecost.com/) (which has since been ported to IBM's web domain), a site receiving 40,000 monthly users. During this time, I grew the total number of web articles by 91%, and increased annual organic traffic to our docs by 43%.

Our docs-as-code pipeline has allowed us to collaborate with the company's multiple engineering teams to deliver accurate and effective documentation, as well as broader process and infrastructure improvements.

### Migration to GitBook

Early on into my role, the company decided to move to a new content management system tool GitBook. The accessibility provided by a WYSIWYG editor could allow for more contributions from non-engineering personnel who may not be as familiar with our docs-as-code tooling. As Kubecost's solo technical writer, I contributed to migration planning calls, acted as the liaison to GitBook's customer support team, and provided training for GitBook to team members. I delivered the training across 7 teams/departments, and ultimately boosted the number of unique docs contributors within the company by 31%.

### Improvements to GitHub Infrastructure

Before joining, our GitHub-backed documentation was a collective effort from engineers who understood quality products require quality documentation. However, there are many subtleties to managing large knowledge bases that do not fall into their expertise or responsibilities. As the technical writer, I launched several initiatives to improve the state of our docs repo and unify its contents into a collective knowledge base.

* Site-wide link checking via GitHub Actions which ran on every pull request to ensure small changes to docs did not later cause large problems. This improved our visibility into page-to-page communication, reducing the potential number of errors caused from moving, replacing, or deleting articles within the repo.
* An automatic triage system for all Issues filed by readers to ensure they received swift attention and resolution. Retroactively sifting through our Issues backlog, I also reduced outstanding user-submitted Issues by 59%.
* Standardized the voice of our docs site through an official Style and Contribution Guide, the first of its kind at Kubecost. This helped reduce minor formatting and language inconsistencies, while also helping us build a cohesive voice for our docs (cannot be shared in this portfolio for confidentiality reasons).

### Contributions to Web Properties

Beyond our technical documentation, I have made additional contributions to Kubecost's other web properties. This includes regular blog posting to showcase new software releases and Kubernetes concepts, as well as minor updates to [OpenCost](https://opencost.io/) documentation, an open-source alternative to Kubecost. Both web properties were hosted in Docusaurus.