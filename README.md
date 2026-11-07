# Duka Analytics Dashboard

Dashibodi ya Streamlit inayochota taarifa za mauzo kutoka MongoDB Atlas.

## Kuendesha ndani ya kompyuta

1. Sakinisha maktaba zilizo kwenye `requirements.txt`.
2. Weka URI ya MongoDB kwenye `.streamlit/secrets.toml` kwa muundo huu:

```toml
[mongo]
uri = "weka-uri-yako-hapa"
```

3. Endesha `streamlit run app.py`.

App hutumia database `duka_db` na collection `mauzo`.

## Streamlit Community Cloud

Weka app kwenye `app.py`, kisha weka `[mongo]` na `uri` kwenye sehemu ya Secrets ya mipangilio ya app. Usipakie `secrets.toml` au faili za credentials kwenye GitHub.
