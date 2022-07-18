select b.uf_sigla, a.periodo, sum(a.frequencia) as quantidade
from nomes a
left join municipios b
on a.local_id = b.id
where b.uf_sigla in ('MG','RJ','SP') and a.nome='LUCAS'
group by b.uf_sigla, a.periodo
order by b.uf_sigla, a.periodo