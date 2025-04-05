import requests

access_token = "AQUN3_Dshl_fGQQHLv18WNDXrUmKUOCmB1Utj1PX3PAaAWzIIOq5zipduaIRcX74ljW16xRftj-29FQnjWE3tBjzP9Z-JN8DmDDWoN8ft5BrpEA-R9oAUasuDBy8zbLNUmejP7suGMyssKz97hR9VYuS4Q5p4enAGioNP4cslf8qLOdiHQf9wEg67tNB_PSzCx43X5i1UbjesMp-gI90E1KhTnxbqjRLfa1gaffRaxZUs96epcuzoLkvbimeYyA2PfOmMabcmcq69hhrYTGJ1o_wQoy_BREtIIAPov5ojcfPpej5Cp28KKcOL204rOKmlJHTwqW3p0V8OcTCPJmdtSLi43RG1A"
headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
response.raise_for_status()

data = response.json()
linkedin_urn = data["id"]

print(linkedin_urn)
