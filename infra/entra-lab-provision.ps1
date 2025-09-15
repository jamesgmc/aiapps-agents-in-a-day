param (
    [string]$subscriptionId, # "xxxxx-xxxx-xxx-xxx",
    [string]$domain, # "xxx.com",
    [string]$labName,  # "lab3"
    [string]$labUserCount = 0
)

# sub-aiaaa
# .\entra-lab-provision.ps1 22f484c3-b754-45aa-8cec-e40bb48bcb34 aiapps.top lab1 3

# sub-aiaaa-lab
# .\entra-lab-provision.ps1 ba15181f-9a45-4eff-9043-4ddf263b6dc2 aiapps.top lab1 3

az account set --subscription $subscriptionId

$EntraIdGroupName = "aad-$labName"

Write-Host "---------Lab--------------"
az ad group create --display-name $EntraIdGroupName --mail-nickname $EntraIdGroupName > $null
Write-Host "Created AAD group $EntraIdGroupName"

$rgSharedName = "rg-$($labName)"
# az group create --name $rgSharedName --location australiaeast > $null
Write-Host "Shared resource group $rgSharedName"

for ($i = 1; $i -le $labUserCount; $i++) {
    Write-Host "---------User--------------"

    $userSeq = $i + 199
    $userName = "$($labName)user$($userSeq)"
    $userEmail = "$($userName)@$($domain)"
    $rgName = "rg-$($userName)"
    
    az ad user create --display-name $userName --password Password123456 --user-principal-name $userEmail --force-change-password-next-sign-in false > $null
    Write-Host "Created user $userName"

    $userId = $(az ad user show --id $userEmail --query id -o tsv)
    az ad group member add --group $EntraIdGroupName --member-id $userId > $null
    Write-Host "Added user $userName to AAD group $EntraIdGroupName"

    az group create --name $rgName --location australiaeast > $null
    Write-Host "Created resource group $rgName"

    # Assign Contributor role to the user for the resource group
    $rgId = $(az group show --name $rgName --query id -o tsv)
    az role assignment create --assignee $userId --role 'Azure AI Developer' --scope $rgId > $null
    az role assignment create --assignee $userId --role 'Azure AI User' --scope $rgId > $null
    az role assignment create --assignee $userId --role 'Contributor' --scope $rgId > $null
    Write-Host "Assigned Contributor role to user $userName for resource group $rgName"
}