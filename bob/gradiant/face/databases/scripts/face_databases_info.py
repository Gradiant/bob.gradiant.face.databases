from bob.gradiant.face.databases import RoseYoutuDatabase, OuluNpuDatabase, ReplayAttackDatabase, ReplayMobileDatabase, \
    UvadDatabase, AggregateDatabase, ThreedmadDatabase, SiwDatabase, CasiaFasdDatabase, HkbuDatabase, CsmadDatabase, \
    MsuMfsdDatabase, CasiaSurfDatabase
from tabulate import tabulate


def main():
    databases = {'3dmad              (grandtest)': ThreedmadDatabase.info(),
                 'aggregate-database (grandtest)': AggregateDatabase.info(),
                 'casia-fasd         (grandtest)': CasiaFasdDatabase.info(),
                 'casia-surf         (grandtest)': CasiaSurfDatabase.info(),
                 'csmad              (grandtest)': CsmadDatabase.info(),
                 'hkbu               (grandtest)': HkbuDatabase.info(),
                 'msu_mfsd           (grandtest)': MsuMfsdDatabase.info(),
                 'oulu_npu           (grandtest)': OuluNpuDatabase.info(),
                 'replay-attack      (grandtest)': ReplayAttackDatabase.info(),
                 'replay-mobile      (grandtest)': ReplayMobileDatabase.info(),
                 'rose-youtu         (grandtest)': RoseYoutuDatabase.info(),
                 'siw                (grandtest)': SiwDatabase.info(),
                 'uvad               (grandtest)': UvadDatabase.info()
                 }

    table = []
    for db in sorted(databases):
        database_row = [db, databases[db]['users'], databases[db]["Train videos"],
                        databases[db]["Dev videos"], databases[db]["Test videos"]]
        table.append(database_row)

    headers = ["Database", "Number of Users", "Train videos", "Dev videos", "Test videos"]
    print("bob.gradiant.face.databases:")
    print(tabulate(table, headers, tablefmt="fancy_grid"))


if __name__ == '__script__':
    main()
