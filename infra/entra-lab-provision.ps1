param (
    [string]$subscriptionId, # "xxxxx-xxxx-xxx-xxx",
    [string]$domain, # "xxx.com",
    [string]$labName,  # "lab3"
    [string]$labUserCount = 0
)

# entra-lab-provision.ps1 9df3a442-42f1-40dd-8547-958c3e01597a aiapps.top lab1 3

az account set --subscription $subscriptionId

$EntraIdGroupName = "aad-$labName"

Write-Host "---------Lab--------------"
az ad group create --display-name $EntraIdGroupName --mail-nickname $EntraIdGroupName > $null
Write-Host "Created AAD group $EntraIdGroupName"

$rgSharedName = "rg-$($labName)-shared"
az group create --name $rgSharedName --location australiaeast > $null
Write-Host "Created shared resource group $rgSharedName"

for ($i = 1; $i -le $labUserCount; $i++) {
    Write-Host "---------User--------------"

    $userSeq = $i
    $userName = "$($labName)User$($userSeq)"
    $userEmail = "$($userName)@$($domain)"
    $rgName = "rg-$($userName)"
    
    az ad user create --display-name $userName --password Password123456 --user-principal-name $userEmail --force-change-password-next-sign-in false > $null
    Write-Host "Created user $userName"

    $userId = $(az ad user show --id $userEmail --query id -o tsv)
    az ad group member add --group aad-lab2 --member-id $userId > $null
    Write-Host "Added user $userName to AAD group $EntraIdGroupName"

    az group create --name $rgName --location australiaeast > $null
    Write-Host "Created resource group $rgName"

    # Assign Contributor role to the user for the resource group
    $rgId = $(az group show --name $rgName --query id -o tsv)
    az role assignment create --assignee $userId --role Contributor --scope $rgId > $null
    Write-Host "Assigned Contributor role to user $userName for resource group $rgName"
}




