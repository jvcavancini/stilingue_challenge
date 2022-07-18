select b.nome, sum(frequencia) as quantidade
from nomes a
left join municipios b
on a.local_id = b.id
where b.uf_sigla='AC' and a.nome='ANA'
group by b.nome
order by sum(frequencia) desc