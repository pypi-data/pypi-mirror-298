# pepe-toolbox

## Before you start

```bash
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
# i don't give a shit about windows
pip install -r requirements.txt
```

## 1. slack_pepe

### How to use

#### 1.1. slack_pepe_webhook

```python
from common_utility_pepe.slack_pepe import SlackPepe

slack_pepe_webhook = SlackPepe.from_webhook(
    webhook_url="your_web_hook_url"
)
slack_pepe_webhook.send_slack_message(title="go away")
```

#### 1.2. slack_pepe_bot

```python
from common_utility_pepe.slack_pepe import SlackPepe

slack_pepe_bot = SlackPepe.from_bot(
    channel="your_channel_id",
    bot_token="your_bot_token"
)
slack_pepe_bot.send_slack_message(title="hi there")

slack_pepe_bot.update_slack_message(timestamp="your_timestamp", title="it's fake")
```
