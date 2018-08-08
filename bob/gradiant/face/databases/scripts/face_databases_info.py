from bob.gradiant.face.databases import MsuMfsdDatabase, OuluNpuDatabase, ReplayAttackDatabase, ReplayMobileDatabase, UvadDatabase, AllPadDatabases
from tabulate import tabulate

def main():
    databases = {'msu_mfsd         (grandtest)': MsuMfsdDatabase.info(),
                 'oulu_npu         (grandtest)': OuluNpuDatabase.info(),
                 'replay-attack    (grandtest)': ReplayAttackDatabase.info(),
                 'replay-mobile    (grandtest)': ReplayMobileDatabase.info(),
                 'uvad             (protocol_1)': UvadDatabase.info(),
                 'all-pad-databases (grandtest)': AllPadDatabases.info()
                 }

    table = []
    for key, value in databases.iteritems():
        database_row = [key, value['users'], value["Train samples"], value["Dev samples"], value["Test samples"]]
        table.append(database_row)

    headers = ["Database", "Number of Users", "Train samples", "Dev samples", "Test Samples"]
    print("bob.gradiant.face.databases:")
    print(tabulate(table, headers, tablefmt="fancy_grid"))


if __name__ == '__script__':
    main()