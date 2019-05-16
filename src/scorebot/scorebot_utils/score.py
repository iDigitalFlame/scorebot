#!/usr/bin/python3
# Scorebot UDP (Universal Development Platform)
#
# The Scorebot Project / iDigitalFlame 2019

from django.db.transaction import atomic
from scorebot_utils.generic import CreateModel


def Event(value, to_team, from_team=None):
    return Transaction(value, "Event", 9, True, to_team, from_team)


def Transfer(value, to_team, from_team=None):
    return Transaction(value, "Transfer", 1, True, to_team, from_team)


def Correction(value, to_team, from_team=None):
    return Transaction(value, "Correction", 0, True, to_team, from_team)


def Achivement(value, to_team, from_team=None):
    return Transaction(value, "Achivement", 8, True, to_team, from_team)


def Transaction(value, type, type_id, save, to_team, from_team=None):
    if value is None:
        return ValueError("value")
    if to_team is None:
        return ValueError("to_team")
    f = from_team
    if f is None:
        f = to_team.GetGame().GoldTeam()
    r, s = None, None
    rs = to_team.GetScore()
    with atomic():
        if rs is not None:
            rc = CreateModel("Credit")
            rc.Type = type_id
            rc.Value = int(value)
            rc.Sender = f
            rc.Receiver = to_team
            rc.Score = rs
            if save:
                rc.save()
            r = CreateModel(type)
            r.Credit = rc
            if save:
                r.save()
                rs.save()
        if from_team is not None:
            fs = from_team.GetScore()
            if fs is not None:
                sc = CreateModel("Credit")
                sc.Type = type_id
                sc.Value = int(value) * -1
                sc.Sender = from_team
                sc.Receiver = to_team
                sc.Score = fs
                if save:
                    sc.save()
                s = CreateModel(type)
                s.Credit = sc
                if save:
                    s.save()
                    fs.save()
    return r, s
