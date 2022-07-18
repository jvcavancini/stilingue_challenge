select * from(
select b.nome as nome_cidade, b.uf_nome, sum(a.frequencia) as quantidade
from nomes a
left join municipios b
on a.local_id = b.id
where a.nome='PEDRO'
group by b.nome, b.uf_nome
order by quantidade desc limit 20
) temp
order by
temp.uf_nome,
temp.nome_cidade