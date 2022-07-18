select a.nome, sum(frequencia) as contagem_nome
from nomes a
left join municipios b
on a.local_id = b.id
where b.nome='Vera Cruz' and b.uf_sigla='SP'
group by a.nome
order by sum(frequencia) asc limit 1