#-*- coding:utf-8 -*-
from openerp.osv import fields, osv

class hr_salary_rule_category(osv.osv):
    """
    HR Salary Rule Category
    """
    
    def _sum_period(self,cr,uid,ids, name,args,context):
        print "===context======",context
        res={}
        for id in ids:
            res[id]=0.0
        return res

    
    def _sum_year(self,cr,uid,ids, name,args,context):
        print "===context======",context
        res={}
        for id in ids:
            res[id]=0.0
        return res

    _inherit = 'hr.salary.rule.category'
    _description = 'Salary Rule Category'
    _columns = {
        'sum': fields.function(_sum_year, string="Year Sum"),
        'sum_period': fields.function(_sum_period, string="Period Sum"),
    }