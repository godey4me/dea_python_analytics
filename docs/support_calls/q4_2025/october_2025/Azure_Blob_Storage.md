## Azure Blob Storage

![](https://user-images.githubusercontent.com/80284865/212203409-7f9660ba-abf1-4a1c-9e86-0d699ed04381.png)

### Description



### Setup Instructions

#### Prereqs
- An Azure subscription and permission to create resources.
- Decide the subscription, resource group, and region you’ll use.

#### A. Create a Storage Account (portal)
1.	In the Azure portal, select Create a resource → Storage account.
2.	Basics tab
- Subscription / Resource group: choose or create.
- Storage account name: globally unique, lower-case letters & numbers.
- Region: pick a region close to your users or data pipelines.
- Performance: Standard (HDD-backed; cost-effective) is typical; Premium adds low-latency options.  ￼
3.	Redundancy: choose LRS (cheapest, single region) or higher (ZRS/GZRS) for more durability/availability.  ￼
4.	Leave other defaults unless you have specific needs → Review + create → Create.  ￼

#### B. Create a Blob Container
1.	Open your new storage account → Data storage → Containers → + Container.
2.	Name: e.g., raw-csv.
3.	Public access level: keep Private (no anonymous access) for most data workloads.
4.	Create.  ￼

> Why a container? All blob data lives inside containers—nothing can be uploaded until one exists.  ￼

#### C. Upload CSV files via the portal
1.	Open your container → Upload.
2.	Drag-and-drop your .csv files or select Browse for files.
3.	(Optional) Set the blob type (default Block blob is correct) and blob tier (Hot/Cool/Archive).
4.	Click Upload to finish.  ￼

#### (Optional) Where to find your connection strings/keys

If you’ll programmatically access blobs later, fetch a connection string under Security + networking → Access keys in the storage account. Keep it secret; prefer managed identities or SAS when possible. 

### Resources

- [Microsoft Documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/blob-containers-portal)
- [Python Workflows with Azure Blob Storage](./Python_Workflows_Azure_Blob_Storage.md)