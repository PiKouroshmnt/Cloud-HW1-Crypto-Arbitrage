"""Module contains constants for Telegram API."""

MESSAGE_TEXT = """
🚨 *Hey!*
I Detected an Arbitrage Opportunity on *{currency_name}*:

*Time:* `{time}`
*Buy:* `${buy_price:.4f}`
*Sell:* `${sell_price:.4f}`
*Profit Percentage:* `{profit_percentage:.2f}%`
*Profit Difference:* `${profit_difference:.4f}`
"""
