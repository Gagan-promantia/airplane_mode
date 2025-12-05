import frappe
from frappe.query_builder import DocType
from frappe.utils import fmt_money



def execute(filters=None):
    if not filters:
        filters = {}

    Airline = DocType("Airline")
    Airplane = DocType("Airplane")
    AirplaneFlight = DocType("Airplane Flight")
    AirplaneTicket = DocType("Airplane Ticket")

    data = []
    total_revenue = 0

    # Get all airlines
    airlines = frappe.get_all("Airline", fields=["name"])

    for airline in airlines:
        # Proper join chain:
        # Airline → Airplane → Airplane Flight → Airplane Ticket
        q = (
            frappe.qb.from_(AirplaneTicket)
            .join(AirplaneFlight)
            .on(AirplaneFlight.name == AirplaneTicket.flight)
            .join(Airplane)
            .on(Airplane.name == AirplaneFlight.airplane)
            .select(AirplaneTicket.total_amount)
            .where(Airplane.airline == airline["name"])
            .where(AirplaneTicket.docstatus == 1)   # only submitted tickets
        )
     
        results = q.run(as_dict=True)
        revenue = sum([r.total_amount or 0 for r in results])
        total_revenue += revenue

        data.append({
            "airline": airline["name"],
            "revenue": revenue,
            # "revenue_fr=ormatted":fmt_money(revenue)
        })

    # Columns
    columns = [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
    ]

    # Donut Chart
    chart = {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [{"values": [d["revenue"] for d in data]}]
        },
        "type": "donut",
        "height": 300
    }

    # Summary
    summary = [
        {"label": "Total Revenue", "value": fmt_money(total_revenue), "indicator": "Green"}
    ]

    return columns, data, None, chart, summary
