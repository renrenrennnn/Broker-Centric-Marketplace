
                    demandSatisfaction = user.calDemandSatisfaction(0.5, broker.ID, user.D_success[broker.ID])
                    if demandSatisfaction < 0.5:
                        y2.append(demandSatisfaction * 2)
                    else:
                        y2.append(demandSatisfaction)