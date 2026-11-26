import JamesTheorems
import Regras
#print axioms James.Conhecimento.amortizacao
#print axioms James.Seguranca.gate
#print axioms James.Alma.replay
#print axioms James.Alma.retomada
#print axioms James.Alma.revezamento
-- Regras de negócio (Regras/): preço da MyBagCenter e etiqueta automática do James Negócio
#print axioms Regras.Preco.abaixo_do_custo_bloqueia_exatamente
#print axioms Regras.Preco.aviso_ml_exato
#print axioms Regras.Preco.aviso_irmaos_exato
#print axioms Regras.Preco.bloqueio_monotono
#print axioms Regras.Preco.aviso_ml_monotono
#print axioms Regras.Preco.aviso_irmaos_monotono
#print axioms Regras.Preco.preco_respeita_piso
#print axioms Regras.Preco.preco_nunca_bloqueado
#print axioms Regras.Preco.preco_monotono_na_ref
#print axioms Regras.Preco.preco_monotono_no_custo
#print axioms Regras.Preco.preco_sem_aviso_ml
#print axioms Regras.Preco.sem_anuncio_cobre_custo
#print axioms Regras.Preco.sem_anuncio_abaixo_do_custo
#print axioms Regras.Etiqueta.nunca_duas_vezes
#print axioms Regras.Etiqueta.nunca_acima_do_teto
#print axioms Regras.Etiqueta.teto_exato
#print axioms Regras.Etiqueta.nao_pago_nao_compra
#print axioms Regras.Etiqueta.saldo_nunca_estoura
#print axioms Regras.Etiqueta.para_no_saldo
