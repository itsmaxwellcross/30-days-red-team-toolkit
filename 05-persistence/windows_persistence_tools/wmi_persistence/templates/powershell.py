"""
PowerShell script templates for WMI persistence operations
"""

# Template for creating WMI event filter
FILTER_TEMPLATE = '''
$FilterArgs = @{{
    name='{filter_name}';
    EventNameSpace='{event_namespace}';
    QueryLanguage="WQL";
    Query="{wql_query}"
}};

$Filter = New-CimInstance -Namespace {subscription_namespace} -ClassName __EventFilter -Property $FilterArgs

Write-Host "[+] Event filter created: {filter_name}"
'''

# Template for creating command line consumer
CONSUMER_TEMPLATE = '''
$ConsumerArgs = @{{
    name='{consumer_name}';
    CommandLineTemplate="{command}"
}};

$Consumer = New-CimInstance -Namespace {subscription_namespace} -ClassName CommandLineEventConsumer -Property $ConsumerArgs

Write-Host "[+] Event consumer created: {consumer_name}"
'''

# Template for creating active script consumer (alternative)
ACTIVE_SCRIPT_CONSUMER_TEMPLATE = '''
$ConsumerArgs = @{{
    name='{consumer_name}';
    ScriptingEngine="VBScript";
    ScriptText="{script_text}"
}};

$Consumer = New-CimInstance -Namespace {subscription_namespace} -ClassName ActiveScriptEventConsumer -Property $ConsumerArgs

Write-Host "[+] Active script consumer created: {consumer_name}"
'''

# Template for binding filter to consumer
BINDING_TEMPLATE = '''
$Filter = Get-CimInstance -Namespace {subscription_namespace} -ClassName __EventFilter -Filter "name='{filter_name}'"
$Consumer = Get-CimInstance -Namespace {subscription_namespace} -ClassName {consumer_class} -Filter "name='{consumer_name}'"

$FilterToConsumerArgs = @{{
    Filter = [Ref]$Filter;
    Consumer = [Ref]$Consumer
}};

$FilterToConsumerBinding = New-CimInstance -Namespace {subscription_namespace} -ClassName __FilterToConsumerBinding -Property $FilterToConsumerArgs

Write-Host "[+] Filter bound to consumer"
'''

# Complete creation template (all-in-one)
COMPLETE_CREATION_TEMPLATE = '''
# Create Event Filter
$FilterArgs = @{{
    name='{filter_name}';
    EventNameSpace='{event_namespace}';
    QueryLanguage="WQL";
    Query="{wql_query}"
}};

$Filter = New-CimInstance -Namespace {subscription_namespace} -ClassName __EventFilter -Property $FilterArgs

# Create Consumer
$ConsumerArgs = @{{
    name='{consumer_name}';
    CommandLineTemplate="{command}"
}};

$Consumer = New-CimInstance -Namespace {subscription_namespace} -ClassName CommandLineEventConsumer -Property $ConsumerArgs

# Bind Filter to Consumer
$FilterToConsumerArgs = @{{
    Filter = [Ref]$Filter;
    Consumer = [Ref]$Consumer
}};

$FilterToConsumerBinding = New-CimInstance -Namespace {subscription_namespace} -ClassName __FilterToConsumerBinding -Property $FilterToConsumerArgs

Write-Host "[+] WMI persistence created successfully"
Write-Host "[+] Filter: {filter_name}"
Write-Host "[+] Consumer: {consumer_name}"
'''

# Template for removing WMI persistence
REMOVAL_TEMPLATE = '''
# Remove Filter
Get-WmiObject -Namespace {subscription_namespace} -Class __EventFilter -Filter "name='{filter_name}'" | Remove-WmiObject

# Remove Consumer
Get-WmiObject -Namespace {subscription_namespace} -Class {consumer_class} -Filter "name='{consumer_name}'" | Remove-WmiObject

# Remove Binding
Get-WmiObject -Namespace {subscription_namespace} -Class __FilterToConsumerBinding | Where-Object {{ $_.Filter.Name -eq '{filter_name}' }} | Remove-WmiObject

Write-Host "[+] WMI persistence removed: {event_name}"
'''

# Template for listing all event filters
LIST_FILTERS_TEMPLATE = '''
Write-Host "=== Event Filters ==="
Get-WmiObject -Namespace {subscription_namespace} -Class __EventFilter | Select-Object Name, Query | Format-List
'''

# Template for listing all consumers
LIST_CONSUMERS_TEMPLATE = '''
Write-Host "=== Command Line Consumers ==="
Get-WmiObject -Namespace {subscription_namespace} -Class CommandLineEventConsumer | Select-Object Name, CommandLineTemplate | Format-List
'''

# Template for listing all bindings
LIST_BINDINGS_TEMPLATE = '''
Write-Host "=== Filter to Consumer Bindings ==="
Get-WmiObject -Namespace {subscription_namespace} -Class __FilterToConsumerBinding | ForEach-Object {{
    $filter = $_.Filter.Name
    $consumer = $_.Consumer.Name
    Write-Host "Filter: $filter -> Consumer: $consumer"
}}
'''

# Complete enumeration template
COMPLETE_ENUMERATION_TEMPLATE = '''
Write-Host "================================================"
Write-Host "WMI Event Subscription Enumeration"
Write-Host "================================================"

Write-Host "`n=== Event Filters ==="
$filters = Get-WmiObject -Namespace {subscription_namespace} -Class __EventFilter
if ($filters) {{
    $filters | Select-Object Name, Query | Format-List
}} else {{
    Write-Host "(none found)"
}}

Write-Host "`n=== Command Line Consumers ==="
$consumers = Get-WmiObject -Namespace {subscription_namespace} -Class CommandLineEventConsumer
if ($consumers) {{
    $consumers | Select-Object Name, CommandLineTemplate | Format-List
}} else {{
    Write-Host "(none found)"
}}

Write-Host "`n=== Active Script Consumers ==="
$scriptConsumers = Get-WmiObject -Namespace {subscription_namespace} -Class ActiveScriptEventConsumer
if ($scriptConsumers) {{
    $scriptConsumers | Select-Object Name, ScriptingEngine, ScriptText | Format-List
}} else {{
    Write-Host "(none found)"
}}

Write-Host "`n=== Filter to Consumer Bindings ==="
$bindings = Get-WmiObject -Namespace {subscription_namespace} -Class __FilterToConsumerBinding
if ($bindings) {{
    $bindings | ForEach-Object {{
        $filter = $_.Filter.Name
        $consumer = $_.Consumer.Name
        Write-Host "  $filter -> $consumer"
    }}
}} else {{
    Write-Host "(none found)"
}}

Write-Host "`n================================================"
'''

# Template for backing up WMI subscriptions
BACKUP_TEMPLATE = '''
$backupData = @{{
    Filters = @();
    Consumers = @();
    Bindings = @()
}}

# Backup Filters
Get-WmiObject -Namespace {subscription_namespace} -Class __EventFilter | ForEach-Object {{
    $backupData.Filters += @{{
        Name = $_.Name
        Query = $_.Query
        EventNameSpace = $_.EventNameSpace
    }}
}}

# Backup Consumers
Get-WmiObject -Namespace {subscription_namespace} -Class CommandLineEventConsumer | ForEach-Object {{
    $backupData.Consumers += @{{
        Name = $_.Name
        CommandLineTemplate = $_.CommandLineTemplate
    }}
}}

# Backup Bindings
Get-WmiObject -Namespace {subscription_namespace} -Class __FilterToConsumerBinding | ForEach-Object {{
    $backupData.Bindings += @{{
        FilterName = $_.Filter.Name
        ConsumerName = $_.Consumer.Name
    }}
}}

$backupData | ConvertTo-Json -Depth 10 | Out-File "{backup_file}"
Write-Host "[+] WMI subscriptions backed up to: {backup_file}"
'''

def generate_creation_script(filter_name, consumer_name, wql_query, command,
                             subscription_namespace='root/subscription',
                             event_namespace='root\\CimV2',
                             consumer_class='CommandLineEventConsumer'):
    """
    Generate complete WMI persistence creation script
    
    Args:
        filter_name (str): Event filter name
        consumer_name (str): Consumer name
        wql_query (str): WQL query
        command (str): Command to execute
        subscription_namespace (str): Subscription namespace
        event_namespace (str): Event namespace
        consumer_class (str): Consumer class type
        
    Returns:
        str: Complete PowerShell script
    """
    return COMPLETE_CREATION_TEMPLATE.format(
        filter_name=filter_name,
        consumer_name=consumer_name,
        wql_query=wql_query,
        command=command,
        subscription_namespace=subscription_namespace,
        event_namespace=event_namespace
    )

def generate_removal_script(filter_name, consumer_name, event_name,
                           subscription_namespace='root\\subscription',
                           consumer_class='CommandLineEventConsumer'):
    """
    Generate WMI persistence removal script
    
    Args:
        filter_name (str): Event filter name
        consumer_name (str): Consumer name
        event_name (str): Event name for display
        subscription_namespace (str): Subscription namespace
        consumer_class (str): Consumer class type
        
    Returns:
        str: Removal PowerShell script
    """
    return REMOVAL_TEMPLATE.format(
        filter_name=filter_name,
        consumer_name=consumer_name,
        event_name=event_name,
        subscription_namespace=subscription_namespace,
        consumer_class=consumer_class
    )

def generate_enumeration_script(subscription_namespace='root\\subscription'):
    """
    Generate complete enumeration script
    
    Args:
        subscription_namespace (str): Subscription namespace
        
    Returns:
        str: Enumeration PowerShell script
    """
    return COMPLETE_ENUMERATION_TEMPLATE.format(
        subscription_namespace=subscription_namespace
    )