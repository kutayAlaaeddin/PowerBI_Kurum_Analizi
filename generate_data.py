"""Generate the fictional portfolio dataset using only the Python standard library."""
import base64
import csv
import gzip
import random
import re
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TABLES = ROOT / "Portfoy.SemanticModel" / "definition" / "tables"
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(4107)
rows = defaultdict(list)
hospitals = ["Demo Ayışığı", "Demo Yelkovan", "Demo Gündönümü", "Demo Bulutkıyı", "Demo Rüzgârvadi"]
branches = ["İç Hastalıkları", "Kardiyoloji", "Göz Hastalıkları", "Ortopedi", "Nöroloji", "Çocuk Sağlığı"]
kinds = ["Pusula", "Prizma", "Yörünge", "Açık Ağ"]
for h, name in enumerate(hospitals, 1):
    rows["dim_hastane"].append([h, name, name])
for b, name in enumerate(branches, 1):
    rows["dim_bolum"].append([b, name])
for patient in range(1, 1501):
    age = rng.randrange(88)
    band = next(label for limit, label in [(5,"0-4"),(18,"5-17"),(40,"18-39"),(65,"40-64"),(100,"65+")] if age < limit)
    rows["dim_hasta"].append([rng.choice(["Kadın","Erkek"]),date(2026-age,1,1),age,band,patient])
start = date(2025,1,1)
end = date(2026,10,19)
month_revenue = defaultdict(int)
month_patients = defaultdict(set)
payer_revenue = defaultdict(int)
i = 0
for offset in range(730):
    day = start + timedelta(days=offset)
    rows["Aktif Gün"].append([day,[1,1,1,1,1,0.5,0][day.weekday()]])
    if day > end:
        continue
    for visit in range(rng.randint(7,19)):
        i += 1
        h = rng.randrange(1,6)
        b = rng.randrange(1,7)
        k = rng.randrange(1,33)
        patient = rng.randrange(1,1501)
        visit_type = rng.choice(["Ayaktan","Ayaktan","Yatış"])
        discharge = min(end, day + timedelta(days=2 if visit_type=="Yatış" else 0))
        payer = f"Demo Ödeyici {k:02}"
        kind = kinds[(k-1)%4]
        category = ["Üye Ağı","Partner Ağı","Proje Ağı","Bağımsız Ağ"][(k-1)%4]
        cash, private, public = rng.randrange(60,350), rng.randrange(600,5600), rng.randrange(30,500)
        total = cash + private + public
        rows["dim_protokol"].append([i,visit_type,day,discharge,k])
        rows["facts_kurum"].append([h,i,patient,b,cash,private,public,total,i,day,cash+10,private+30,public,total+40])
        service = total + rng.randrange(100,1500)
        rows["facts_hizmet"].append([h,b,service,branches[b-1],day,day])
        period = day.replace(day=1)
        month_patients[h,period].add(patient)
        month_revenue[h,period] += total
        payer_revenue[k] += total
        if i%13 == 0:
            continue
        billed = discharge + timedelta(days=1)
        fee = private + 30
        tax, cut, refund = fee//100, fee//80, 0
        net = fee-tax-cut-refund
        paid = [net,net//2,0][i%3]
        status = ["Ödenen","Kısmi Ödenen","Ödenmeyen"][i%3]
        rows["facts_fatura"].append([i,h,900000+i,billed,billed+timedelta(days=9) if paid else None,
            800000+i//8,billed,billed+timedelta(days=1),billed+timedelta(days=30),status,day,discharge,
            i,tax,fee,cut,refund,paid,net-paid,billed if i%4 else None,"Fatura Edildi" if i%4 else "Fatura Edilmedi",
            category,payer+" "+kind,payer,kind,kind,visit_type,branches[b-1],k])
for rank,k in enumerate(sorted(payer_revenue,key=payer_revenue.get,reverse=True),1):
    payer = f"Demo Ödeyici {k:02}"
    index = (k-1)%4
    kind = kinds[index]
    rows["dim_kurum"].append([k,payer,["Üye Ağı","Partner Ağı","Proje Ağı","Bağımsız Ağ"][index],payer+" "+kind,kind,kind,rank,str(index+1)])
for h,name in enumerate(hospitals,1):
    for year in [2025,2026]:
        for month in range(1,13):
            period = date(year,month,1)
            base = month_revenue.get((h,period),250000)
            target = round(base*rng.uniform(.91,1.13))
            rows["Bütçe"].append([h,period,target,name,round(target*1.24)])
            patients = month_patients.get((h,period))
            if patients:
                rows["Hizmet Hasta Sayısı"].append([len(patients)+rng.randrange(5,20),period,h])

# Embed the same CSV in Power Query so moving the project never breaks refresh.
m_types = {"string":"type text","int64":"Int64.Type","double":"type number","dateTime":"type date","decimal":"Currency.Type"}
for table, records in rows.items():
    file = TABLES / (table+".tmdl")
    definition = file.read_text(encoding="utf-8")
    columns = []
    for block in re.split(r"(?m)^\t(?=column |partition |measure )",definition):
        if not block.startswith("column "):
            continue
        name = re.search(r"(?m)^\t\tsourceColumn: (.+)$",block)
        if name:
            datatype = re.search(r"(?m)^\t\tdataType: (.+)$",block)[1]
            columns.append((name[1],m_types[datatype]))
    assert all(len(row)==len(columns) for row in records),table
    output = DATA / (table+".csv")
    with output.open("w",encoding="utf-8",newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow([name for name,_ in columns])
        writer.writerows(records)
    encoded = base64.b64encode(gzip.compress(output.read_bytes(),mtime=0)).decode()
    chunks = [encoded[n:n+16000] for n in range(0,len(encoded),16000)]
    binary = " &\n\t\t\t        ".join('"'+chunk+'"' for chunk in chunks)
    types = ", ".join('{"'+name+'", '+typ+'}' for name,typ in columns)
    source = ("\n\t\t\tlet\n\t\t\t    Payload = "+binary+",\n"
              "\t\t\t    Bytes = Binary.Decompress(Binary.FromText(Payload, BinaryEncoding.Base64), Compression.GZip),\n"
              '\t\t\t    Csv = Csv.Document(Bytes, [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n'
              "\t\t\t    Headers = Table.PromoteHeaders(Csv),\n"
              '\t\t\t    Clean = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),\n'
              '\t\t\t    Typed = Table.TransformColumnTypes(Clean, {'+types+'}, "en-US")\n\t\t\tin\n\t\t\t    Typed\n')
    match = re.search(r"(\n\tpartition [^\n]+ = m\n[\s\S]*?\n\t\tsource =)[\s\S]*?(?=\n\tannotation |\Z)",definition)
    assert match,table
    file.write_text(definition[:match.start()]+match[1]+source+definition[match.end():],encoding="utf-8")
