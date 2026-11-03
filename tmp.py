change = False
            for i in range(2):
                if p1_within:
                    tracker += 1
                    if p1[i] != p2[i]:
                        if p1[i] > p2[i]:
                            p1[i] = pmax_x
                        else:
                            p1[i] = pmin_x
                    else:
                        if p1[i] > p3[i]:
                            p1[i] = pmax_x
                        else:
                            p1[i] = pmin_x

                if p2_within:
                    tracker += 1
                    if p2[i] != p3[i]:
                        if p2[i] > p3[i]:
                            p2[i] = pmax_x
                        else:
                            p2[i] = pmin_x
                    else:
                        if p2[i] > p3[i]:
                            p2[i] = pmax_x
                        else:
                            p2[i] = pmin_x

                if p3_within:
                    tracker += 1
                    if p3[i] != p1[i]:
                        if p3[i] > p1[i]:
                            p3[i] = pmax_x
                        else:
                            p3[i] = pmin_x
                    else:
                        if p3[i] > p2[i]:
                            p3[i] = pmax_x
                        else:
                            p3[i] = pmin_x