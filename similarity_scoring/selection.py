import DBOperation
import umbc_scoring
import FYPsetting
from kld_scoring import KLDistance

for target in FYPsetting.TARGET_LIST:

    kld_obj=KLDistance()
    date_today = 20160425
    selected_candidates = []
    chosen_list = []
    new_article_list = []
    for i in range(FYPsetting.COMPARING_DATES):
        chosen_list.extend(DBOperation.query_chosen(str(date_today-i), target))
        new_article_list.extend(DBOperation.query_articles(str(date_today-i), target))

    umbc_threshold = FYPsetting.SIMI_THRESHOLD
    kld_threshold = FYPsetting.KLD_THRESHOLD

    for new_article in new_article_list:
        sim = 0
        cov = 0
        new_title = new_article[1]
        new_source = new_article[3]
        new_body = new_article[4]
        for chosen_article in chosen_list:
            chosen_title = chosen_article[1]
            chosen_source = chosen_article[3]
            chosen_body = chosen_article[4]
            if 1 in ((new_source == chosen_source and new_source == 'NYT'), (new_source == chosen_source and new_source == 'NASDAQ')):
                continue
            else:
                u_score = umbc_scoring.umbc_sim(new_title, chosen_title)
                if u_score > umbc_threshold:
                    sim=1
                    break
                else:
                    kld1,kld2 = kld_obj.kl_divergence(new_body,chosen_body)
                    if kld1<kld_threshold and kld2<kld_threshold:
                        sim=1
                        break
                    elif kld1>kld_threshold and kld2>kld_threshold:
                        pass
                    elif kld1-kld2<kld_threshold:
                        sim=1
                    elif kld1-kld2>kld_threshold:
                        cov=1
                        chosen_list.append(new_article)
                        chosen_list.remove(chosen_article)
                        break
        if sim==1:
            continue
        elif cov==1:
            continue
        else:
            chosen_list.append(new_article)

    DBOperation.update_selection(chosen_list, date_today, target)



