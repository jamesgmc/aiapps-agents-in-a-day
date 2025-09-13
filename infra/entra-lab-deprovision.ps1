param (
    [string]$subscriptionId, # "xxxxx-xxxx-xxx-xxx",
    [string]$domain, # "xxx.com",
    [string]$labName,  # "lab3"
    [string]$labUserCount = 0
)

az account set --subscription $subscriptionId

$EntraIdGroupName = "aad-$labName"

for ($i = 1; $i -le $labUserCount; $i++) {
    Write-Host "---------User--------------"

    $userSeq = $i
    $userName = "$($labName)User$($userSeq)"
    $userEmail = "$($userName)@$($domain)"
    $rgName = "rg-$($labName)-$($userName)"
    $userId = $(az ad user show --id $userEmail --query id -o tsv)

    az ad user delete --id $userId
    Write-Host "Deleted user $userName"
    az group delete --name $rgName -y
    Write-Host "Deleted resource group $rgName"
}

Write-Host "---------Lab--------------"
$rgSharedName = "rg-$($labName)-shared"
az group delete --name $rgSharedName -y
Write-Host "Deleted shared resource group $rgSharedName"

$EntraIdGroupId = $(az ad group show --group $EntraIdGroupName --query id -o tsv)
az ad group delete -g $EntraIdGroupId
Write-Host "Deleted AAD group $EntraIdGroupName"


