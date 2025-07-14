

```
curl https://glvd.ingress.glvd.gardnlinux.shoot.canary.k8s-hana.ondemand.com/v1/cves/1592.4 | jq -r '.[] | select(.vulnerable==true) | .cveId'
```
