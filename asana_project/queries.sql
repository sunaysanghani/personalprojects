ASANA_DATA.PUBLIC.USER_INFO/*using sql for basic cleaning **/

select name, email from user_info group by name, email having count(*) > 1;

delete from user_info where id in (select name, email from user_info group by name, email having count(*) > 1;);


--exploratory data analysis
select creation_source, count(*) as count_by_creation_source from user_info group by creation_source;
select count(*) user_id_referrals from user_info where invited_by_user_id is not null;


--segmentation
create view segmented_customer_view as
select user_id, case
    when visit_count between 20 and 70 then 'mid count visitor'
    when visit_count > 70 then 'high count visitor'
    else 'low count visitor'
    end as segment
from (select user_id, count(*) as visit_count from user_visited group by user_id) as user_engagement;


select * from segmented_customer_view where segment = 'high count visitor';

create view valued_customers1 as
select id
from (select invited_by_user_id as id from user_info group by invited_by_user_id having count(*) > 5) as invited;

select * from valued_customers1;


-- Which user segments (based on creation_source, opted_in_to_mailing_list, and enabled_for_marketing_drip) have the highest conversion rates?
select u.creation_source, sum(m.conversions) as conversion_rates
from marketing_campaigns m
inner join user_info u on m.user_id = u.object_id
group by u.creation_source
order by conversion_rates desc;

-- Which marketing campaigns resulted in the highest user engagement?
select o.campaign_name, sum(o.conversions) as sum_conversions
from org_marketing_campaigns o
group by o.campaign_name
order by sum_conversions desc;

--What is the ROI of each marketing campaign considering the budget spent and the number of conversions achieved?
select o.campaign_name, sum(o.conversions)/sum(o.budget) * 100 as ROI_percentage
from org_marketing_campaigns o
group by o.campaign_name
order by ROI_percentage desc;


--How does user engagement differ between users who were part of marketing campaigns and those who were not?
select u.org_id
from user_info u
where u.org_id not in (select org_id from org_marketing_campaigns)

