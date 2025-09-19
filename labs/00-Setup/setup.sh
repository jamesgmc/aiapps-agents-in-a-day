#!/bin/bash

CONFIG_URL="https://aiaaa-s2-setting.azurewebsites.net/api/configuration/all"

echo "Fetching configuration from $CONFIG_URL..."
config_json=$(curl -s "$CONFIG_URL")

if [ -z "$config_json" ]; then
    echo "Failed to fetch configuration."
    exit 1
fi

# Extract all key-value pairs from the JSON without jq
declare -A replacements
# Remove outer braces and split by commas
config_clean=$(echo "$config_json" | sed 's/^{//; s/}$//' | tr ',' '\n')
while IFS= read -r line; do
    if [[ $line =~ \"([^\"]+)\"[[:space:]]*:[[:space:]]*\"([^\"]*)\"|\"([^\"]+)\"[[:space:]]*:[[:space:]]*([^,}]+) ]]; then
        if [[ -n "${BASH_REMATCH[1]}" ]]; then
            key="${BASH_REMATCH[1]}"
            value="${BASH_REMATCH[2]}"
        else
            key="${BASH_REMATCH[3]}"
            value="${BASH_REMATCH[4]}"
            # Remove quotes if present
            value=$(echo "$value" | sed 's/^"//; s/"$//')
        fi
        replacements["<$key>"]="$value"
    fi
done <<< "$config_clean"

echo "Searching for .env files..."

find ../../ -type f \( -name "*.env" \) -not -path "*/node_modules/*" | while read -r file; do
    echo "Processing: $file"
    for search in "${!replacements[@]}"; do
        replace=$(echo "${replacements[$search]}" | sed 's/&/\\&/g')
        sed -i "s|${search}|${replace}|g" "$file"
    done
done

echo "Replacements complete!"