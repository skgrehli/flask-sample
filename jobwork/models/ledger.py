import datetime

from jobwork.db_connection import db
from jobwork.utils.common_utils import CommonUtils


# noinspection SpellCheckingInspection
class Ledgers(object):
    @classmethod
    def find(cls, *args, **kwargs):
        return db.ledgers.find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return db.ledgers.find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return db.ledgers.update(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return db.ledgers.insert(*args, **kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        return db.ledgers.count(*args, **kwargs)

    @classmethod
    def bid_selection_entries(cls, userid, jobid, bidid, final_bid, payment_details):
        total_bid_amount = float(final_bid['bidamount'])
        commission = float(total_bid_amount * 0.1)
        final_bidamount = float(total_bid_amount - commission)

        cls.insert({
            "userid": userid,
            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
            "amount": float(total_bid_amount) * (-1),
            "datetime": datetime.datetime.now(),
            "type": "ESCROW",
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "paymentdetailsJSON": payment_details,
            "refunddetailsJSON": "",
            "refundcompletiondatetime": "",
            "payingdatetime": "",
            "remark": "",
            "active": True
        })

        cls.insert({
            "userid": userid,
            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
            "amount": float(commission),
            "datetime": datetime.datetime.now(),
            "type": "COMMISSION",
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "paymentdetailsJSON": "",
            "refunddetailsJSON": "",
            "refundcompletiondatetime": "",
            "payingdatetime": "",
            "remark": "",
            "active": True})

        cls.insert({
            "userid": final_bid["userid"],
            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
            "amount": float(final_bidamount),
            "datetime": datetime.datetime.now(),
            "type": "PAID",
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "paymentdetailsJSON": "",
            "refunddetailsJSON": "",
            "refundcompletiondatetime": "",
            "payingdatetime": "",
            "remark": "",
            "active": True
        })

    @classmethod
    def bid_reverse_entries(cls, userid, jobid, bidid, final_bid, payment_details):
        total_bid_amount = float(final_bid['bidamount'])
        commission = float(total_bid_amount * 0.1)
        final_bidamount = float(total_bid_amount - commission)

        cls.insert({
            "userid": userid,
            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
            "amount": float(total_bid_amount) * (-1),
            "datetime": datetime.datetime.now(),
            "type": "ESCROW",
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "paymentdetailsJSON": payment_details,
            "refunddetailsJSON": "",
            "refundcompletiondatetime": "",
            "payingdatetime": "",
            "remark": "",
            "active": True})

        cls.insert({
            "userid": userid,
            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
            "amount": float(commission),
            "datetime": datetime.datetime.now(),
            "type": "COMMISSION",
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "paymentdetailsJSON": "",
            "refunddetailsJSON": "",
            "refundcompletiondatetime": "",
            "payingdatetime": "",
            "remark": "",
            "active": True})

        cls.insert({
            "userid": final_bid['userid'],
            "ledgerid": CommonUtils.generateRandomNo(Ledgers, "ledgerid"),
            "amount": float(final_bidamount),
            "datetime": datetime.datetime.now(),
            "type": "PAID",
            "jobid": int(jobid),
            "jobbidid": int(bidid),
            "paymentdetailsJSON": "",
            "refunddetailsJSON": "",
            "refundcompletiondatetime": "",
            "payingdatetime": "",
            "remark": "",
            "active": True})
