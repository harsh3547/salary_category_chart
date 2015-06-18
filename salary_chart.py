#-*- coding:utf-8 -*-
from openerp.osv import fields, osv

class hr_salary_rule_category(osv.osv):
    """
    HR Salary Rule Category
    """
    
    def _sum_period(self,cr,uid,ids, name,args,context):
        #print "\n\n===period==context======",context
        res={}
        for id in ids:
            res[id]=0.0
        #print "-----------res orginal",res
            
        present_period_id = self.pool.get('account.period').find(cr, uid, context=context)
        period_id = context.get('period_obj',False) or (present_period_id and present_period_id[0]) or False
        state = context.get('state',False) or 'done' 
        if period_id and state:
            #print "=========period_id,state==",period_id,state
            cr.execute("select id from hr_payslip where date_to >= (select date_start from account_period where id = %s) and date_to <= (select date_stop from account_period where id = %s) and state = %s",(period_id,period_id,state,))
            payslip_ids=tuple([i[0] for i in cr.fetchall()])
            #print "0-0-0-0-0-payslip_ids=====",payslip_ids
            if not payslip_ids:return res
            cr.execute("select category_id,total from hr_payslip_line where slip_id in %s",(payslip_ids,))
            categ_total=cr.fetchall()
            #print "-0-0-0-0-0--categ_total-",categ_total
            for val in categ_total:
                id=val[0]
                amount=val[1]
                parent_id=True
                while parent_id != None:
                    res[id] =res[id] + amount if res.get(id,False) else amount
                    cr.execute("select parent_id from hr_salary_rule_category where id = %s",(id,))
                    parent_id=cr.fetchall()[0][0]
                    id=parent_id
        #print "----------------0-0-0 final value",res
        return res

    
    def _sum_year(self,cr,uid,ids, name,args,context):
        #print "\n\n\n===context==========year====",context
        res={}
        for id in ids:
            res[id]=0.0
        #print "-----------res orginal",res
        
        fiscalyear_id = self.pool.get('account.fiscalyear').finds(cr, uid, exception=False)
        presentyear_id = context.get('fiscalyear_id',False) or (fiscalyear_id and fiscalyear_id[0]) or False
        state = context.get('state',False) or 'done' 
        if presentyear_id and state:
            #print "=========presentyear_id,state==",presentyear_id,state
            cr.execute("select id from hr_payslip where date_to >= (select date_start from account_fiscalyear where id = %s) and date_to <= (select date_stop from account_fiscalyear where id = %s) and state = %s",(presentyear_id,presentyear_id,state,))
            payslip_ids=tuple([i[0] for i in cr.fetchall()])
            #print "0-0-0-0-0-payslip_ids=====",payslip_ids
            if not payslip_ids:return res
            cr.execute("select category_id,total from hr_payslip_line where slip_id in %s",(payslip_ids,))
            categ_total=cr.fetchall()
            #print "-0-0-0-0-0--categ_total-",categ_total
            for val in categ_total:
                id=val[0]
                amount=val[1]
                parent_id=True
                while parent_id != None:
                    res[id] =res[id] + amount if res.get(id,False) else amount
                    cr.execute("select parent_id from hr_salary_rule_category where id = %s",(id,))
                    parent_id=cr.fetchall()[0][0]
                    id=parent_id
        #print "----------------0-0-0 final value",res
        return res


    _inherit = 'hr.salary.rule.category'
    _description = 'Salary Rule Category'
    _columns = {
        'sum': fields.function(_sum_year, string="Year Sum"),
        'sum_period': fields.function(_sum_period, string="Period Sum"),
    }