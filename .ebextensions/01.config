files:
    "/etc/httpd/conf.d/ssl_rewrite.conf":
        mode: "000644"
        owner: root
        group: root
        content: |
            RewriteEngine On
            <If "-n '%{HTTP:X-Forwarded-Proto}' && %{HTTP:X-Forwarded-Proto} != 'https'">
            RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [R,L]
            </If>