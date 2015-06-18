# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class salary_categ_chart(osv.osv_memory):
    _name = "salary.categ.chart"
    _description = "Salary Category Chart"
    _columns = {
       'period_id': fields.many2one('account.period','Period'),
       'target_move': fields.selection([('done', 'All Confirmed Entries'),
                                        ('draft', 'All Draft Entries'),
                                        ], 'State', required=True),
    }
    
    def _get_period(self, cr, uid, context=None):
        """Return default period value"""
        period_ids = self.pool.get('account.period').find(cr, uid, context=context)
        return period_ids and period_ids[0] or False

    def salary_chart_open_window(self, cr, uid, ids, context=None):

        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        result = mod_obj.get_object_reference(cr, uid, 'hr_payroll', 'action_hr_salary_rule_category_tree_view')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        if data.period_id:
            result['context'] = str({'period_obj': data.period_id.id,'state': data.target_move,'fiscalyear_id': data.period_id.fiscalyear_id.id})
            period_code = data.period_id.code
        else:
            result['context'] = str({'state': data.target_move})
        
        ###print "---------------result--------------",result
        return result

    
    
    _defaults = {
        'period_id': _get_period,
        'target_move': 'done'
    }
