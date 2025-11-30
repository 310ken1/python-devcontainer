"""."""

import aws_cdk
from BackendStack import BackendStack

app = aws_cdk.App()
BackendStack(app, "BackendStack")
app.synth()
