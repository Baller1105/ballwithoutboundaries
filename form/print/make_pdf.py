"""Builds the printable, branded Sports Money DNA questionnaire PDF."""
import base64, pathlib, subprocess, json
root = pathlib.Path(__file__).resolve().parents[2]
logo = "data:image/png;base64," + base64.b64encode((root/"brand/bwb-logo-full-web.png").read_bytes()).decode()
mark = "data:image/png;base64," + base64.b64encode((root/"brand/bwb-wordmark-web.png").read_bytes()).decode()

PAY = ["Out of the regular paycheck (month to month)","Savings we set aside specifically for sports","General savings or emergency fund",
"Credit card, paid off in full each month","Credit card, carrying a balance","Buy now, pay later (Klarna, Afterpay, Affirm…)",
"The club's or program's payment plan","Home equity line (HELOC) or home equity loan","Cash-out refinance on our home","Personal loan",
"Borrowing from or withdrawing from a 401(k) or retirement account","Money from grandparents or family","Second job, overtime or a side hustle",
"Fundraising, sponsorships or scholarships","Selling things","Something else: ________________"]
A = [
 ("How many of your kids play organized sports right now?", "one", ["1","2","3","4+"], 4),
 ("What level is your most competitive athlete playing at?", "one", ["Rec / community","School team","Club / travel","Elite / national / showcase","Multiple levels"], 2),
 ("Roughly how much does your family spend on youth sports per year, all-in? (All kids: fees, travel, hotels, gear, lessons, food on the road.)", "one",
   ["Under $1,000","$1,000 – $2,500","$2,500 – $5,000","$5,000 – $10,000","$10,000 – $20,000","$20,000+","Honestly, I don't know"], 2),
 ("Which is the biggest single cost?", "one", ["Club or team fees","Travel & hotels","Private lessons or training","Camps & clinics","Equipment & uniforms","Tournament & showcase fees","Food on the road"], 2),
 ("THE KEY QUESTION: How do you pay for it?", "all", PAY, 2),
 ("Of everything you checked above, which ONE pays for the most?", "line", [], 1),
 ("How much of your family's debt right now is because of youth sports?", "one", ["None","Less than $1,000","$1,000 – $5,000","$5,000 – $15,000","$15,000 – $30,000","$30,000+","Not sure"], 2),
 ("To pay for sports, have you cut back on any of these?", "all", ["Retirement contributions","College savings (529, etc.)","Emergency savings","Family vacations","Home repairs","Our own health or medical care","Paying down other debt","None of these"], 2),
 ("How stressful is paying for sports for your family?", "scale", [], 5),
 ("Be honest: would you ever pull your child out of a sport because of money?", "one", ["No, we'll find a way","Only if we truly had no choice","We've considered it","We've already had to"], 2),
 ("Do you and your partner ever disagree about sports spending?", "one", ["Never","Sometimes","Often","It's a big source of tension","Not applicable"], 2),
 ("If someone could help with ONE thing, what would it be?", "one", ["Lowering the cost of sports","Paying off the debt it created","Planning ahead for next season","Getting on the same page with my partner","Finding scholarships & sponsorships","Protecting retirement & college savings"], 2),
]
B = [
 ("Household income range (optional)", "one", ["Under $50K","$50K – $75K","$75K – $100K","$100K – $150K","$150K – $250K","$250K+","Prefer not to say"], 2),
 ("What's your child's main sport, and at what age did spending really take off?", "line", [], 1),
 ("If you used home equity, a refinance, a personal loan or retirement money, roughly how much went to sports?", "one", ["Didn't use these","Under $5K","$5K – $15K","$15K – $30K","$30K – $50K","$50K+"], 2),
 ("Do you know the interest rate on the debt you use for sports?", "one", ["Yes, exactly","Roughly","No idea","No debt"], 4),
 ("At your current pace, how long until your sports-related debt is paid off?", "one", ["Paid off monthly","Under 6 months","6 – 12 months","1 – 3 years","3+ years","Never at this rate"], 2),
 ("Do you plan ahead for the season, or handle costs as they come?", "one", ["We plan the whole year","We plan somewhat","We handle it as it comes","Bills surprise us every season"], 2),
 ("What's driving the spending most?", "one", ["My child's love of the game","College scholarship hopes","Keeping up with the team","Coach or club pressure","Development & training needs","Pro aspirations"], 2),
 ("Do you believe the spending will \"pay back\" (scholarship, pro, etc.)?", "one", ["Yes, definitely","Maybe","Probably not, and that's OK","I don't think about it that way"], 2),
 ("In one sentence: what do you wish you'd known about the cost before you started?", "lines", [], 1),
 ("Want a founding seat or a 15-minute follow-up? (optional)", "contact", [], 1),
]
DNA = [("🎯","The Planner","#38B259","Pays from savings set aside for sports.","Sharpen the edges: travel hacks, team-buy gear, multi-season plan."),
("💪","The Cash-Flow Grinder","#1DADE0","Pays month to month from the paycheck.","Build a Season Fund. That's your first ONE BILL."),
("💳","The Card Swiper","#C9C23A","Uses a card, pays it off in full.","Set a season cap; point rewards at team travel."),
("🔁","The Balance Carrier","#F5A524","Carries a card balance, BNPL or payment plans.","Your ONE bill is the card: payoff plan and a rate you know."),
("🏠","The Equity Tapper","#FF7A59","HELOC, cash-out refi or personal loan.","Know what the borrowing costs; plan so the house isn't funding next season."),
("⏳","The Future Borrower","#9B6CF0","401(k) money or cut retirement contributions.","Protect retirement first; then scholarships and a funding plan."),
("🤝","The Village-Funded","#2E9A4C","Grandparents, side hustles, fundraising.","Make it sustainable for when the help changes.")]

def box(round_=False): return f'<span class="bx{" rd" if round_ else ""}"></span>'
def q_html(n, q, kind, opts, cols, deep=False):
    key = q.startswith("THE KEY")
    title = q.replace("THE KEY QUESTION: ","")
    head = f'<div class="qh"><div class="jer"><svg viewBox="0 0 64 70"><path d="M18 4 L26 2 Q32 10 38 2 L46 4 L62 14 L56 28 L50 25 L50 68 L14 68 L14 25 L8 28 L2 14 Z" fill="{"#1DADE0" if deep else "#38B259"}" stroke="#10233F" stroke-width="3" stroke-linejoin="round"/></svg><b>{n}</b></div><div>' + \
      (f'<div class="key">The key question · check ALL that apply</div>' if key else (f'<div class="sub">Check all that apply</div>' if kind=="all" else (f'<div class="sub">Choose one</div>' if kind=="one" else ""))) + f'<h3>{title}</h3></div></div>'
    body = ""
    if kind in ("one","all"):
        body = f'<div class="opts c{cols}">' + "".join(f'<div class="o">{box(kind=="one")}<span>{o}</span></div>' for o in opts) + '</div>'
    elif kind=="scale":
        labels=["No stress","Fine","It's tight","Hard","Keeps me up at night"]
        body = '<div class="scale">' + "".join(f'<div class="s">{box(True)}<b>{i+1}</b><small>{labels[i]}</small></div>' for i in range(5)) + '</div>'
    elif kind=="line": body = '<div class="ln"></div>'
    elif kind=="lines": body = '<div class="ln"></div><div class="ln"></div>'
    elif kind=="contact":
        body = '<div class="ct"><div>First name<div class="ln"></div></div><div>Email<div class="ln"></div></div></div><div class="opts c2"><div class="o">'+box()+'<span>🏆 Tell me about becoming a Founding Member</span></div><div class="o">'+box()+'<span>📞 Open to a 15-minute follow-up call</span></div></div>'
    return f'<section class="q{" kq" if key else ""}">{head}{body}</section>'

qa = "".join(q_html(i+1,*x) for i,x in enumerate(A))
qb = "".join(q_html(i+13,*x, deep=True) for i,x in enumerate(B))
dna = "".join(f'<div class="d" style="--c:{c}"><div class="de">{e}</div><div><h4>{n}</h4><p><b>Pays by:</b> {w}</p><p><b>Next play:</b> {p}</p></div></div>' for e,n,c,w,p in DNA)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
@page {{ size: Letter; margin: 0.45in 0.5in 0.55in; }}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,Arial,sans-serif;color:#10233F;font-size:10.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.D{{font-family:'Saira Condensed',Impact,sans-serif;font-weight:900;font-style:italic;text-transform:uppercase}}
.cover{{height:9.85in;border-radius:22px;overflow:hidden;position:relative;color:#F4FAFB;padding:.55in .55in;
 background:radial-gradient(700px 400px at 10% -10%,rgba(29,173,224,.35),transparent 60%),radial-gradient(700px 400px at 100% 0,rgba(56,178,89,.3),transparent 60%),linear-gradient(180deg,#10233F,#0B1A31);page-break-after:always}}
.cover .turf{{position:absolute;left:0;right:0;bottom:0;height:1.0in;background:repeating-linear-gradient(90deg,#1f7a3c 0 .55in,#23863f .55in 1.1in);opacity:.9}}
.cover .turf::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.35) 0 2px,transparent 2px 1.1in)}}
.cover .logo{{display:block;width:3.9in;margin:0 auto .15in;background:radial-gradient(ellipse at center,#F4FAFB 0 58%,rgba(244,250,251,0) 72%);padding:.25in .35in}}
.eb{{font-family:'Saira Condensed';font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:#38B259;font-size:11pt;text-align:center}}
.cover h1{{font-size:42pt;line-height:.92;text-align:center;margin:.12in 0 .2in}}
.cover h1 em{{color:#38B259}}
.cover p.lead{{font-size:12.5pt;line-height:1.55;text-align:center;color:#D9E3EF;max-width:6.2in;margin:0 auto}}
.stats,.trust,.how,.cover h1,.cover p,.eb,.logo{{position:relative;z-index:2}}
.stats{{display:flex;gap:.15in;margin:.3in 0 .2in}}
.stat{{flex:1;background:rgba(10,22,40,.6);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:.14in;text-align:center}}
.stat b{{display:block;font-size:26pt;color:#EEE865}} .stat span{{font-size:9pt;color:#9FB0C6}}
.trust{{text-align:center;font-size:10pt;color:#CFE0EE}} .trust span{{margin:0 .1in}} .trust span::before{{content:"✓ ";color:#38B259;font-weight:800}}
.how{{margin:.22in auto 0;max-width:6.4in;background:rgba(10,22,40,.85);border:2px solid #38B259;border-radius:16px;padding:.16in .22in;font-size:10pt;line-height:1.5;color:#E8F0F7}}
.how b{{color:#38B259}}
.src{{position:absolute;bottom:.12in;font-weight:600;left:0;right:0;text-align:center;font-size:8pt;color:#E8F0F7;z-index:2}}
.bar{{display:flex;align-items:center;justify-content:space-between;background:#10233F;color:#F4FAFB;border-radius:14px;padding:.1in .18in;margin-bottom:.16in}}
.bar img{{height:.42in;background:#F4FAFB;padding:3px 8px;border-radius:8px}}
.bar .t{{font-size:18pt}} .bar .t em{{color:#38B259}} .bar .p{{font-family:'Saira Condensed';font-weight:800;letter-spacing:.14em;font-size:9pt;color:#EEE865;text-transform:uppercase}}
.q{{border:1.5px solid #D6DEE8;border-radius:14px;padding:.12in .16in .14in;margin-bottom:.12in;page-break-inside:avoid;background:#fff}}
.kq{{border:2.5px solid #38B259;background:linear-gradient(180deg,#F1FBF4,#fff)}}
.qh{{display:flex;gap:.12in;align-items:center;margin-bottom:.08in}}
.jer{{width:.5in;height:.55in;position:relative;flex:none}} .jer svg{{position:absolute;inset:0}}
.jer b{{position:absolute;inset:0;display:grid;place-items:center;padding-top:.08in;font-family:'Saira Condensed';font-weight:900;font-style:italic;font-size:16pt;color:#10233F}}
h3{{font-size:11.5pt;line-height:1.3;font-weight:700}}
.sub{{font-family:'Saira Condensed';font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:8pt;color:#6B7F99}}
.key{{font-family:'Saira Condensed';font-weight:800;letter-spacing:.14em;text-transform:uppercase;font-size:8.5pt;color:#2E9A4C}}
.opts{{display:grid;gap:.05in .18in}} .c2{{grid-template-columns:1fr 1fr}} .c4{{grid-template-columns:repeat(4,1fr)}} .c1{{grid-template-columns:1fr}}
.o{{display:flex;gap:.08in;align-items:flex-start;font-size:10pt;line-height:1.3;padding:.03in 0}}
.bx{{flex:none;width:.16in;height:.16in;border:1.8px solid #10233F;border-radius:4px;margin-top:1px}} .bx.rd{{border-radius:50%}}
.scale{{display:flex;justify-content:space-between;gap:.1in}} .s{{flex:1;text-align:center;border:1.5px solid #D6DEE8;border-radius:10px;padding:.07in}}
.s .bx{{margin:0 auto .04in}} .s b{{display:block;font-family:'Saira Condensed';font-weight:900;font-style:italic;font-size:18pt}} .s small{{font-size:8pt;color:#6B7F99}}
.ln{{border-bottom:1.5px solid #9FB0C6;height:.32in;margin-top:.04in}}
.ct{{display:grid;grid-template-columns:1fr 1.4fr;gap:.2in;margin-bottom:.08in;font-size:9pt;color:#6B7F99}}
.divider{{text-align:center;margin:.06in 0 .14in;padding:.14in;border-radius:14px;background:#10233F;color:#F4FAFB;page-break-before:always}}
.divider h2{{font-size:24pt}} .divider p{{font-size:10pt;color:#CFE0EE;margin-top:.04in}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:.12in}}
.d{{display:flex;gap:.12in;border:2px solid var(--c);border-radius:14px;padding:.12in;page-break-inside:avoid}}
.de{{font-size:24pt}} .d h4{{font-family:'Saira Condensed';font-weight:900;font-style:italic;text-transform:uppercase;font-size:15pt;color:var(--c)}}
.d p{{font-size:9pt;line-height:1.4;margin-top:.03in}}
.fine{{font-size:8pt;color:#6B7F99;text-align:center;margin-top:.16in;line-height:1.5}}
.thanks{{margin-top:.18in;text-align:center;padding:.2in;border-radius:16px;background:linear-gradient(135deg,#38B259,#1DADE0);color:#10233F}}
.thanks h2{{font-size:22pt}} .thanks p{{font-size:10.5pt;font-weight:600;margin-top:.05in}}
</style></head><body>
<div class="cover"><div class="turf"></div>
 <img class="logo" src="{logo}">
 <div class="eb">The Sports Money DNA · 4 minutes</div>
 <h1 class="D">How does your family <em>really</em> pay for the game?</h1>
 <p class="lead">Every report says youth sports costs keep climbing, and that a lot of families "go into debt." But nobody has asked <b>how</b>. Credit cards? Home equity? A second job? Grandma? We're finding out, so we can help sports families keep their kids playing <b>without wrecking everything else.</b></p>
 <div class="stats"><div class="stat"><b class="D">+46%</b><span>rise in what families spend on a child's main sport since 2019</span></div>
 <div class="stat"><b class="D">$40B+</b><span>spent by parents on youth sports every year</span></div>
 <div class="stat"><b class="D">?</b><span>how families actually pay for it. Until now.</span></div></div>
 <div class="trust"><span>Anonymous if you want</span><span>Never sold, ever</span><span>Shared only as group totals</span></div>
 <div class="how"><b>How it works:</b> Part A is 12 quick questions. Part B, the Deep Dive, is optional. Check the boxes, then find your family's <b>Sports Money DNA</b> type on the last page.</div>
 <div class="src">Stats: Aspen Institute Project Play, 2024 parent survey.</div>
</div>
<div class="bar"><img src="{mark}"><div class="t D">Part A · <em>The Quick DNA</em></div><div class="p">Questions 1–12</div></div>
{qa}
<div class="divider"><h2 class="D">Part B · The Deep Dive</h2><p>Optional, about 5 more minutes. This is the data that helps us crack the code for every sports family.</p></div>
{qb}
<div class="divider"><h2 class="D">Find your Sports Money DNA</h2><p>Look at your answer to Question 6 (what pays for the most). That's your type.</p></div>
<div class="dgrid">{dna}</div>
<div class="thanks"><h2 class="D">Thank you for playing.</h2><p>Ball Without Boundaries: where sports meets the financial intelligence to fund it.</p></div>
<p class="fine">Educational only, not individual financial, tax, insurance or legal advice. Your answers are private and only shared as anonymous group totals. We never sell your data.<br>© Ball Without Boundaries</p>
</body></html>"""
out = root/"form/print/sports-money-dna-print.html"
out.write_text(html)
print(out)
