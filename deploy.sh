# Load env variables
eval "$(cat .env <(echo) <(declare -x))"

# Download all dependency and pack them as zip file
pipenv run pip install -r <(pipenv lock -r) --target deploy/
cp -R src deploy
cd deploy
zip -r source.zip *
hash=`openssl md5 source.zip | awk '{print $2}'`
echo "source.zip: hash = $hash"
filename="${hash}.zip"
mv source.zip $filename

# Upload zip file to s3 bucket
s3_keyname="${FunctionName}/${filename}"
aws s3 cp $filename s3://${BucketName}/${FunctionName}/

# Create cloud formation template
cp ../sam_template.yml ./
aws cloudformation package \
    --template-file sam_template.yml \
    --s3-bucket ${BucketName} \
    --output-template-file packaged-${FunctionName}.yml

# Deploy by cloud formation
aws cloudformation deploy \
    --template-file packaged-${FunctionName}.yml \
    --stack-name ${FunctionName}-lambda  \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        BucketName=${BucketName} \
        CodeKey=${s3_keyname} \
        CompanyMailAddress=${CompanyMailAddress} \
        CompanyName=${CompanyName} \
        CorporateSiteDomain=${CorporateSiteDomain} \
        SesEndpointUrl=${SesEndpointUrl}

# remove dir
cd ..
rm -r deploy