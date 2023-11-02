# dl4g-donnschtig-jass

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/damman01/dl4g-donnschtig-jass)

https://github.com/thomas-koller/jass-kit-py

## DEPLOYMENT to fl0

main branch will automatically deploy to [fl0 - https://dl4g-donnschtig-jass-dev-cqsg.1.ie-1.fl0.io](https://dl4g-donnschtig-jass-dev-cqsg.1.ie-1.fl0.io)

[fl{/} Server:  https://app.fl0.com/damman01/schelle-Uusli/dev/dl4g-donnschtig-jass](https://app.fl0.com/damman01/schelle-Uusli/dev/dl4g-donnschtig-jass)

Logs: https://app.fl0.com/damman01/schelle-Uusli/dev/dl4g-donnschtig-jass/logs

## Run locally

```uvicorn main:app --proxy-headers --host=0.0.0.0 --port=8090```