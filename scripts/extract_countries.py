import json

with open(r'c:\Users\garet\Desktop\funeral-repatriation\site\data\countries_repatriation.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

exclude = {'spain', 'thailand', 'usa', 'turkey', 'india'}

# Standard keys present in excluded countries
standard_keys = set()
for c in [v for k, v in data['countries'].items() if k in exclude]:
    standard_keys.update(c.keys())

result = {}
for key, c in data['countries'].items():
    if key in exclude:
        continue

    proc = c.get('repatriation_process', {})
    s1 = proc.get('step_1_immediate', {})
    s2 = proc.get('step_2_death_certificate', {})
    s5 = proc.get('step_5_coffin', {})
    s6 = proc.get('step_6_documentation', {})
    ca = c.get('content_angles', {})
    at = c.get('ashes_transport', {})
    pm = c.get('post_mortem', {})
    tl = c.get('typical_timeline', {})
    cg = c.get('cost_guide', {})

    unique_fields = {k: c[k] for k in c.keys() if k not in standard_keys}

    entry = {
        'name': c.get('name'),
        'slug': c.get('slug'),
        'death_volume_rank': c.get('death_volume_rank'),
        'british_deaths_per_year_est': c.get('british_deaths_per_year_est'),
        'typical_timeline_average_case': tl.get('average_case'),
        'cost_guide_total_typical_range_gbp': cg.get('total_typical_range_gbp'),
        'content_angles_primary_angle': ca.get('primary_angle'),
        'content_angles_unique_selling_points': (ca.get('unique_selling_points') or [])[:3],
        'content_angles_common_complications': (ca.get('common_complications') or [])[:5],
        'step_1_immediate_details': s1.get('details'),
        'step_2_death_certificate': {
            'shows_cause_of_death': s2.get('shows_cause_of_death'),
            'multilingual_available': s2.get('multilingual_available'),
            'only_one_original': s2.get('only_one_original'),
            'local_term': s2.get('local_term'),
            'processing_time': s2.get('processing_time'),
        },
        'step_5_coffin_notes': s5.get('notes'),
        'step_6_documentation_notes': s6.get('notes'),
        'post_mortem_when_required': pm.get('when_required'),
        'post_mortem_impact_on_timeline': pm.get('impact_on_timeline'),
        'ashes_transport_cremation_available': at.get('cremation_available'),
        'ashes_transport_critical_warning': at.get('critical_warning'),
        'unique_fields': unique_fields if unique_fields else None,
    }
    result[key] = entry

sorted_result = dict(sorted(result.items(), key=lambda x: (x[1]['death_volume_rank'] is None, x[1]['death_volume_rank'] or 999)))

with open(r'c:\Users\garet\Desktop\funeral-repatriation\country_extract.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_result, f, indent=2, ensure_ascii=False)

# Print summary table
header = f"{'Key':<22} {'Name':<28} {'Rank':<5} {'Deaths/yr':<15} {'Timeline':<22} {'Cost GBP':<28} Unique fields"
print(header)
print('-' * 140)
for key, entry in sorted_result.items():
    uf = list(entry['unique_fields'].keys()) if entry['unique_fields'] else []
    print(f"{key:<22} {entry['name']:<28} {str(entry['death_volume_rank']):<5} {str(entry['british_deaths_per_year_est']):<15} {str(entry['typical_timeline_average_case']):<22} {str(entry['cost_guide_total_typical_range_gbp']):<28} {uf}")

print()
print(f'Total: {len(sorted_result)} countries')
print(f'Written to: country_extract.json')
