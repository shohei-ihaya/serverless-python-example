role_name="codebuild-serverless-python-service-role"

if ! arn=`aws iam get-role --role-name ${role_name} | jq -r .Role.Arn`; then
    arn=`aws iam create-role --role-name ${role_name} --assume-role-policy-document file://assume-role-policy.json | jq -r .Role.Arn`
    aws iam attach-role-policy --role-name ${role_name} --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
else
    echo "The role named ${role_name} already exists"
fi

escaped_arn=$(echo $arn | sed -e 's/\:/\\:/g' | sed -e 's/\//\\\//g')
sed -e "s/serviceRoleArn/$escaped_arn/" codebuild_template.json > codebuild.json

aws codebuild create-project --cli-input-json file://codebuild.json
rm codebuild.json

aws codebuild create-webhook --project-name serverless-python

build_id=`aws codebuild start-build --project-name serverless-python | jq -r .build.id`
aws codebuild batch-get-builds --ids ${build_id}
