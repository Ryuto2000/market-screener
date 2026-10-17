import yfinance as yf, traceback
for t in ["7203.T", "6758.T", "AAPL"]:
    print("=====", t)
    tk = yf.Ticker(t)
    for attr in ["quarterly_income_stmt", "quarterly_financials", "income_stmt"]:
        try:
            q = getattr(tk, attr)
            print(attr, None if q is None else q.shape)
            if q is not None and not q.empty:
                print([str(c.date()) for c in q.columns][:6])
                print([i for i in q.index if "Revenue" in i or "Operating Income" in i][:6])
        except Exception:
            print(attr, "ERR", traceback.format_exc()[-300:])
    try:
        print("calendar", tk.calendar)
    except Exception as e:
        print("calendar err", e)
