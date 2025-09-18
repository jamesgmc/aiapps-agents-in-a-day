#!/bin/bash

CONFIG_URL="https://aiaaa-s2-setting.azurewebsites.net/api/configuration/all"

echo "Fetching configuration from $CONFIG_URL..."
config_json=$(curl -s "$CONFIG_URL")

if [ -z "$config_json" ]; then
    echo "Failed to fetch configuration."
    exit 1
fi

# Extract all key-value pairs from the JSON
declare -A replacements
while IFS="=" read -r key value; do
    replacements["<$key>"]="$value"
done < <(echo "$config_json" | jq -r 'to_entries[] | "\(.key)=\(.value)"')

echo "Searching for .env, .js, and setup.sh files..."

find /workspaces/aiapps-agents-in-a-day -type f \( -name "*.env" -o -name "*.js" -o -name "setup.sh" \) -not -path "*/node_modules/*" | while read -r file; do
    echo "Processing: $file"
    for search in "${!replacements[@]}"; do
        replace=$(echo "${replacements[$search]}" | sed 's/&/\\&/g')
        sed -i "s|${search}|${replace}|g" "$file"
    done
done

echo "Replacements complete!"