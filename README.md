
---

#  README

All components run via **docker-compose** using the prebuilt image as required.

---

##  1. Download this repository

Clone or download the repository to your machine.

---

##  2. Pull the Docker image

```bash
docker pull madhavprasad2003/kasparromain:latest
```

---

##  3. Setup environment variables

```bash
cp .env.example .env
```

---

##  4. Start the application

### Normal start:

```bash
docker-compose up
```

### To start CoinGeckoAPI:

```bash
API_KEY=Your_API_Key docker-compose up
```

---

## API Endpoints

Once started, the application exposes:

```
http://0.0.0.0:8000/xyz
```

Where:

* `xyz = stats, data, health`

The ETL pipeline also runs automatically.

---

##  Example Query

Retrieve entries **from 10th December** and go to **page 4**:

```
http://0.0.0.0:8000/data?page=4&from_ts="2025-12-10"
```

Parameter details can be found in `api/main.py`.

---

## Running Tests

1. Start the app:

   ```bash
   docker-compose up
   ```

2. Then run tests:

   ```bash
   docker-compose exec app python -m pytest -q ./tests
   ```

---

## Please Note

1. The CSV under `data/csv` is used as a tiny placeholder source.
2. ETL workers could be separated per source for independence (not implemented due to time constraints).
3. The failure-recovery test is incomplete as of now.
4. Cloud deployment is done on GCP.

### Cloud API Endpoint

```
https://etl-api-617963497994.us-central1.run.app/stats
```

---

## 📞 Contact Information

*Please note that I am currently unable to receive calls on the number provided in the Google forms.
If needed, please message me on WhatsApp. Thank you.*

---
