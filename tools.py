from typing import Dict,Any

def Calculate_Vehicle_duty(cif_value:float,engine_cc:int,fule:str):
    """
    Computes customs duty based on Indian import tariff rules:
    - Electric Vehicles: 70% basic customs duty
    - High-displacement (>3000cc) or high-value (>30 Lakh): 100% luxury duty
    - Standard passenger vehicles: 60% basic customs duty
    - Social Welfare Surcharge (SWS): 10% on Basic Customs Duty (BCD)
    """

    fule=fule.lower()
    duty=0
    is_luxuary=False
    if(fule=="electric"):
        duty=0.07
        if cif_value>=4000000:
            is_luxuary=True
    elif(engine_cc>=3000 or cif_value>=3000000):
        duty=1
        if cif_value>=3000000:
            is_luxuary=True
        else:
            is_luxuary=False

    bcd=cif_value*duty
    sws=bcd*0.10
    total_duty=bcd+sws
    landed_cost = cif_value + total_duty


    return {
        "duty_rate_percent": duty * 100,
        "basic_customs_duty": round(bcd, 2),
        "social_welfare_surcharge": round(sws, 2),
        "total_duty_payable": round(total_duty, 2),
        "final_landed_cost": round(landed_cost, 2),
        "is_luxury_bracket": is_luxuary
    }


