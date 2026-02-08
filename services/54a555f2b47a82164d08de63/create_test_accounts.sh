#!/bin/bash
# AsyncHBase is a client library for HBase and does not have its own
# user management system. User authentication is handled by HBase itself.
# This script is a placeholder - user accounts must be created in HBase
# or the Kerberos/LDAP identity provider that HBase is configured to use.

echo "AsyncHBase does not manage user accounts directly."
echo "User authentication is handled by the HBase cluster security configuration:"
echo "  - For simple auth: configure hbase.security.simple.username in asynchbase.conf"
echo "  - For Kerberos: Use your organization's Kerberos identity management"