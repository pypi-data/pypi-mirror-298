
from diagrams import Diagram, Cluster

from diagrams.aws.management import Organizations, OrganizationsAccount, OrganizationsOrganizationalUnit
from diagrams.aws.general import Users, User

with Diagram("SSO-State", show=False, direction="TB"):
    gg = Users("Group")
    uu= User("User")

    with Cluster('Groups'):

        gg_0= Users("AWSSecurityAudit\nPowerUsers")

        gg_1= Users("AWSLogArchiveAdm\nins")

        with Cluster("SecOps_Adms"):

                gg_2= [User("w.alejovl+secops\n-labs@gmail.com"),]

        gg_3= Users("AWSLogArchiveVie\nwers")

        with Cluster("AWSControlTowerAdmins"):

                gg_4= [User("velez94@protonma\nil.com"),]

        with Cluster("DevSecOps_Admins"):

                gg_5= [User("DevSecOpsAdm"),]

        gg_6= Users("AWSSecurityAudit\nors")

        with Cluster("AWSAccountFactory"):

                gg_7= [User("velez94@protonma\nil.com"),]

        gg_8= Users("AWSAuditAccountA\ndmins")

        gg_9= Users("AWSServiceCatalo\ngAdmins")
