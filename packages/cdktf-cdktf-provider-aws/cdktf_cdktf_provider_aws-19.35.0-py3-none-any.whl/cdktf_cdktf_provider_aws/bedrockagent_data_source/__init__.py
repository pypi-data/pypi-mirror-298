r'''
# `aws_bedrockagent_data_source`

Refer to the Terraform Registry for docs: [`aws_bedrockagent_data_source`](https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class BedrockagentDataSource(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSource",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source aws_bedrockagent_data_source}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        knowledge_base_id: builtins.str,
        name: builtins.str,
        data_deletion_policy: typing.Optional[builtins.str] = None,
        data_source_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["BedrockagentDataSourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vector_ingestion_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source aws_bedrockagent_data_source} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param knowledge_base_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#knowledge_base_id BedrockagentDataSource#knowledge_base_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#name BedrockagentDataSource#name}.
        :param data_deletion_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#data_deletion_policy BedrockagentDataSource#data_deletion_policy}.
        :param data_source_configuration: data_source_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#data_source_configuration BedrockagentDataSource#data_source_configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#description BedrockagentDataSource#description}.
        :param server_side_encryption_configuration: server_side_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#server_side_encryption_configuration BedrockagentDataSource#server_side_encryption_configuration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#timeouts BedrockagentDataSource#timeouts}
        :param vector_ingestion_configuration: vector_ingestion_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#vector_ingestion_configuration BedrockagentDataSource#vector_ingestion_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499da3284ad1f3481c99bcbd79758f3c78e47f604b996226e6bff6cb2641b0f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = BedrockagentDataSourceConfig(
            knowledge_base_id=knowledge_base_id,
            name=name,
            data_deletion_policy=data_deletion_policy,
            data_source_configuration=data_source_configuration,
            description=description,
            server_side_encryption_configuration=server_side_encryption_configuration,
            timeouts=timeouts,
            vector_ingestion_configuration=vector_ingestion_configuration,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a BedrockagentDataSource resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BedrockagentDataSource to import.
        :param import_from_id: The id of the existing BedrockagentDataSource that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BedrockagentDataSource to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7280012840639152b759fa042c3572c225b8865b2eff7f3224af16ca056f2885)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDataSourceConfiguration")
    def put_data_source_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19560266da7143f13dd4aa6febbb9a386282a3bbdfbe6a1fbe39fd3dc1b19045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataSourceConfiguration", [value]))

    @jsii.member(jsii_name="putServerSideEncryptionConfiguration")
    def put_server_side_encryption_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14839d87ddf30e9a12b452cb7d6147d893edc8e21ea8bf5106476bb37e40c1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServerSideEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#create BedrockagentDataSource#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#delete BedrockagentDataSource#delete}
        '''
        value = BedrockagentDataSourceTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVectorIngestionConfiguration")
    def put_vector_ingestion_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8ed8a2df48e466b68173a80d202d12924c7a7d2ec880c42025feed292993a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVectorIngestionConfiguration", [value]))

    @jsii.member(jsii_name="resetDataDeletionPolicy")
    def reset_data_deletion_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataDeletionPolicy", []))

    @jsii.member(jsii_name="resetDataSourceConfiguration")
    def reset_data_source_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSourceConfiguration", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetServerSideEncryptionConfiguration")
    def reset_server_side_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerSideEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVectorIngestionConfiguration")
    def reset_vector_ingestion_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVectorIngestionConfiguration", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceConfiguration")
    def data_source_configuration(
        self,
    ) -> "BedrockagentDataSourceDataSourceConfigurationList":
        return typing.cast("BedrockagentDataSourceDataSourceConfigurationList", jsii.get(self, "dataSourceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> "BedrockagentDataSourceServerSideEncryptionConfigurationList":
        return typing.cast("BedrockagentDataSourceServerSideEncryptionConfigurationList", jsii.get(self, "serverSideEncryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BedrockagentDataSourceTimeoutsOutputReference":
        return typing.cast("BedrockagentDataSourceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="vectorIngestionConfiguration")
    def vector_ingestion_configuration(
        self,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationList":
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationList", jsii.get(self, "vectorIngestionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="dataDeletionPolicyInput")
    def data_deletion_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataDeletionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceConfigurationInput")
    def data_source_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfiguration"]]], jsii.get(self, "dataSourceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseIdInput")
    def knowledge_base_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "knowledgeBaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfigurationInput")
    def server_side_encryption_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceServerSideEncryptionConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceServerSideEncryptionConfiguration"]]], jsii.get(self, "serverSideEncryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BedrockagentDataSourceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BedrockagentDataSourceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vectorIngestionConfigurationInput")
    def vector_ingestion_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfiguration"]]], jsii.get(self, "vectorIngestionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataDeletionPolicy")
    def data_deletion_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataDeletionPolicy"))

    @data_deletion_policy.setter
    def data_deletion_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da415da3b18aa16a19a9aa00c4bf6c2640680f1b35b4bda8bbc87f5da846949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataDeletionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c789628668987a09cdda7ef7a0656bda6a8005e73b69ee384b10513e761d4a70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="knowledgeBaseId")
    def knowledge_base_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseId"))

    @knowledge_base_id.setter
    def knowledge_base_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af829b6389ff95731ad16302f79d827c0909f6a83b0619d74f4b178763f091eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "knowledgeBaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f12b586bc5fd427d7b3114bec93476ffa3a9509c703b843e40ea06c1badbe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "knowledge_base_id": "knowledgeBaseId",
        "name": "name",
        "data_deletion_policy": "dataDeletionPolicy",
        "data_source_configuration": "dataSourceConfiguration",
        "description": "description",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "timeouts": "timeouts",
        "vector_ingestion_configuration": "vectorIngestionConfiguration",
    },
)
class BedrockagentDataSourceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        knowledge_base_id: builtins.str,
        name: builtins.str,
        data_deletion_policy: typing.Optional[builtins.str] = None,
        data_source_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceDataSourceConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceServerSideEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["BedrockagentDataSourceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vector_ingestion_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param knowledge_base_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#knowledge_base_id BedrockagentDataSource#knowledge_base_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#name BedrockagentDataSource#name}.
        :param data_deletion_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#data_deletion_policy BedrockagentDataSource#data_deletion_policy}.
        :param data_source_configuration: data_source_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#data_source_configuration BedrockagentDataSource#data_source_configuration}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#description BedrockagentDataSource#description}.
        :param server_side_encryption_configuration: server_side_encryption_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#server_side_encryption_configuration BedrockagentDataSource#server_side_encryption_configuration}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#timeouts BedrockagentDataSource#timeouts}
        :param vector_ingestion_configuration: vector_ingestion_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#vector_ingestion_configuration BedrockagentDataSource#vector_ingestion_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BedrockagentDataSourceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2df85ee439b62a35399d661f3574eb62b06cc43b81ec6d3247dfd59fdf447cc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument data_deletion_policy", value=data_deletion_policy, expected_type=type_hints["data_deletion_policy"])
            check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vector_ingestion_configuration", value=vector_ingestion_configuration, expected_type=type_hints["vector_ingestion_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "knowledge_base_id": knowledge_base_id,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if data_deletion_policy is not None:
            self._values["data_deletion_policy"] = data_deletion_policy
        if data_source_configuration is not None:
            self._values["data_source_configuration"] = data_source_configuration
        if description is not None:
            self._values["description"] = description
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vector_ingestion_configuration is not None:
            self._values["vector_ingestion_configuration"] = vector_ingestion_configuration

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def knowledge_base_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#knowledge_base_id BedrockagentDataSource#knowledge_base_id}.'''
        result = self._values.get("knowledge_base_id")
        assert result is not None, "Required property 'knowledge_base_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#name BedrockagentDataSource#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_deletion_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#data_deletion_policy BedrockagentDataSource#data_deletion_policy}.'''
        result = self._values.get("data_deletion_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfiguration"]]]:
        '''data_source_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#data_source_configuration BedrockagentDataSource#data_source_configuration}
        '''
        result = self._values.get("data_source_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfiguration"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#description BedrockagentDataSource#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceServerSideEncryptionConfiguration"]]]:
        '''server_side_encryption_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#server_side_encryption_configuration BedrockagentDataSource#server_side_encryption_configuration}
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceServerSideEncryptionConfiguration"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BedrockagentDataSourceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#timeouts BedrockagentDataSource#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BedrockagentDataSourceTimeouts"], result)

    @builtins.property
    def vector_ingestion_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfiguration"]]]:
        '''vector_ingestion_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#vector_ingestion_configuration BedrockagentDataSource#vector_ingestion_configuration}
        '''
        result = self._values.get("vector_ingestion_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceDataSourceConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "s3_configuration": "s3Configuration"},
)
class BedrockagentDataSourceDataSourceConfiguration:
    def __init__(
        self,
        *,
        type: builtins.str,
        s3_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceDataSourceConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#type BedrockagentDataSource#type}.
        :param s3_configuration: s3_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#s3_configuration BedrockagentDataSource#s3_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a53260b5eda595cd7f287dee58d19e5f2e1e38f3db9b35078991b4886a91a2f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if s3_configuration is not None:
            self._values["s3_configuration"] = s3_configuration

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#type BedrockagentDataSource#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfigurationS3Configuration"]]]:
        '''s3_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#s3_configuration BedrockagentDataSource#s3_configuration}
        '''
        result = self._values.get("s3_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfigurationS3Configuration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceDataSourceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceDataSourceConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceDataSourceConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83723fe6725bc85d420b5f41e422b123738dadea0d0d2908e91cd03417eb9050)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceDataSourceConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8385c422e57ab149b420f48407873e1706bb42d11e3169b7ed1e321f2694fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceDataSourceConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac55f4df787f679c9994ce232dde4b8bfe8f860a2b81a0a5f98ea804e79f1a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0247ffecb90087ec4345189e7557500c62798b12acce2cd723a7414261a22823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1193f6eedd1640c22441459499178b0072e4077f27e9e05ae5e521698479ab9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08381c1cb3f696e4aed39440c481379aaf132fa31005dfecff03fca02fef72b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceDataSourceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceDataSourceConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3962d119ad0eb7585fd5cda968c6c1741b3a18c5940fd2bd03110a2169cb7dbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putS3Configuration")
    def put_s3_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceDataSourceConfigurationS3Configuration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d0d0342c5ba48607d21fd2e721f6303ffe75bd2c290a1dffadf0b86a8315bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putS3Configuration", [value]))

    @jsii.member(jsii_name="resetS3Configuration")
    def reset_s3_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Configuration", []))

    @builtins.property
    @jsii.member(jsii_name="s3Configuration")
    def s3_configuration(
        self,
    ) -> "BedrockagentDataSourceDataSourceConfigurationS3ConfigurationList":
        return typing.cast("BedrockagentDataSourceDataSourceConfigurationS3ConfigurationList", jsii.get(self, "s3Configuration"))

    @builtins.property
    @jsii.member(jsii_name="s3ConfigurationInput")
    def s3_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfigurationS3Configuration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceDataSourceConfigurationS3Configuration"]]], jsii.get(self, "s3ConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e45f76bcf902a0defd3f603e1e44e2dcd6a05d9e54c4c38786ea0b82e89ad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7feebe0d4712b7020dc65dc6f236afe601987996bd45c47dbfc690c6df92ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceDataSourceConfigurationS3Configuration",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "bucket_owner_account_id": "bucketOwnerAccountId",
        "inclusion_prefixes": "inclusionPrefixes",
    },
)
class BedrockagentDataSourceDataSourceConfigurationS3Configuration:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        bucket_owner_account_id: typing.Optional[builtins.str] = None,
        inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#bucket_arn BedrockagentDataSource#bucket_arn}.
        :param bucket_owner_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#bucket_owner_account_id BedrockagentDataSource#bucket_owner_account_id}.
        :param inclusion_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#inclusion_prefixes BedrockagentDataSource#inclusion_prefixes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be09d318ee91b8038bed7ab3191c81f1fea450260e388b6bafbe34322372404)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument bucket_owner_account_id", value=bucket_owner_account_id, expected_type=type_hints["bucket_owner_account_id"])
            check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
        }
        if bucket_owner_account_id is not None:
            self._values["bucket_owner_account_id"] = bucket_owner_account_id
        if inclusion_prefixes is not None:
            self._values["inclusion_prefixes"] = inclusion_prefixes

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#bucket_arn BedrockagentDataSource#bucket_arn}.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_owner_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#bucket_owner_account_id BedrockagentDataSource#bucket_owner_account_id}.'''
        result = self._values.get("bucket_owner_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#inclusion_prefixes BedrockagentDataSource#inclusion_prefixes}.'''
        result = self._values.get("inclusion_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceDataSourceConfigurationS3Configuration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceDataSourceConfigurationS3ConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceDataSourceConfigurationS3ConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b3c650dbb69943787a9277964cf71e7e7a93ce336b41607b428f6a50a10eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceDataSourceConfigurationS3ConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807a84d3edbf75f4586c76cce7ffe5bf36983fe67e71a811e0f0a480fcbccbed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceDataSourceConfigurationS3ConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf39eb595202cef18d9027dc0154823313754fcf927cfee5b83b2eeeebf7c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55f822415f0aa218717f05372f2490f1dc887695c1842b9d9704240b905ad20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83b49a69f07684cd41ac4868f56ba4233bd2acf0146b9e12cb5727ef9e31f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfigurationS3Configuration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfigurationS3Configuration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfigurationS3Configuration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b429364b0aa9acec05982b8cf28153ecb2739a5f6dd06c10760f6180775735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceDataSourceConfigurationS3ConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceDataSourceConfigurationS3ConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504950f1cea4c5646870b528191304d02a78929b3499303888989a00bbf03c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBucketOwnerAccountId")
    def reset_bucket_owner_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketOwnerAccountId", []))

    @jsii.member(jsii_name="resetInclusionPrefixes")
    def reset_inclusion_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusionPrefixes", []))

    @builtins.property
    @jsii.member(jsii_name="bucketArnInput")
    def bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccountIdInput")
    def bucket_owner_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketOwnerAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionPrefixesInput")
    def inclusion_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inclusionPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @bucket_arn.setter
    def bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32c28c449efef35027d18857f6b4db5c746b901645027927cdfa9f8a9161c653)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bucketOwnerAccountId")
    def bucket_owner_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketOwnerAccountId"))

    @bucket_owner_account_id.setter
    def bucket_owner_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e963405ee51a96cba8f4cc2e38882876108f9e3dc13c12f5a13f4e92ea31ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketOwnerAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inclusionPrefixes")
    def inclusion_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inclusionPrefixes"))

    @inclusion_prefixes.setter
    def inclusion_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc1061ebc3c9102e46617eeeb34df6f89c7c970cde7b99ab4cc7501cc938cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inclusionPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfigurationS3Configuration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfigurationS3Configuration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfigurationS3Configuration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7a501f33f9b294efe6c0df37f648773408461db7932e45baba80aa6b2c2a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceServerSideEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn"},
)
class BedrockagentDataSourceServerSideEncryptionConfiguration:
    def __init__(self, *, kms_key_arn: typing.Optional[builtins.str] = None) -> None:
        '''
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#kms_key_arn BedrockagentDataSource#kms_key_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86df8e9c1018ef4b06b6422efcc721c56db31415cf4af17bfc256968a7c02cd4)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#kms_key_arn BedrockagentDataSource#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceServerSideEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceServerSideEncryptionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceServerSideEncryptionConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8dfaa8af5aaef2a77b465459a284eff91658b2e8e9ba9bae1f857de3d8221f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceServerSideEncryptionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de23e9714ff0a2453fbfb621dcc4187b4b30dd0923dd75e7d024cac29d6a00d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceServerSideEncryptionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1d53f3bd5837d7de666ebfbf2e1c497ab869817eee4ee4ce453ffe8ce2aaad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d4e8f93bea1f9a9fb8bd95338131a2c10d4bccb2b793eff178c845ad7d9602)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b571bb3093705db7474b25967298c24acf2235766c8036bbc294930ed4ea484d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceServerSideEncryptionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceServerSideEncryptionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceServerSideEncryptionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aed545102bcb68ffc55298aefdce7d5e20cdbee33192b78ffc33bc8dfb6d8a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceServerSideEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceServerSideEncryptionConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f492837cd84eff243ff6a6a75727880e829eb39318675e487bc01d6cec1e6812)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d145fa975730aff6b1e161a5aa6b4b5ee331e451277f914793d8a6c53156d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceServerSideEncryptionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceServerSideEncryptionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceServerSideEncryptionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42aa785c624c26bade26f03e536aab991652ea52c60f53fc6ee5696045c6ad93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class BedrockagentDataSourceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#create BedrockagentDataSource#create}
        :param delete: A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#delete BedrockagentDataSource#delete}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da42f6a13d38feeef76a411967f6705b91883dba3dd8a12b073c8906956acf1c)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#create BedrockagentDataSource#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''A string that can be `parsed as a duration <https://pkg.go.dev/time#ParseDuration>`_ consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#delete BedrockagentDataSource#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567fca939951ec876941ce6cafe11d30d3c6933ecb29d1d8f59def92f67a4870)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f2ee45214c3a22b1a2fb4241be52b7452c8760ff015522172b0f9f65401ae2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cdb5e4ce5de8289e4fe2652ee891c0689f01a2cb600d2698ec12819a8a33a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2ae89fc74d7d919227d3812c37215c6d81a4c4c5d6e99d0ee506f16ba500a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "chunking_configuration": "chunkingConfiguration",
        "parsing_configuration": "parsingConfiguration",
    },
)
class BedrockagentDataSourceVectorIngestionConfiguration:
    def __init__(
        self,
        *,
        chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parsing_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chunking_configuration: chunking_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#chunking_configuration BedrockagentDataSource#chunking_configuration}
        :param parsing_configuration: parsing_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_configuration BedrockagentDataSource#parsing_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70149422f201a4edffcb7a4a9b980760573b6faf9dee871ed67b58e3fe90935c)
            check_type(argname="argument chunking_configuration", value=chunking_configuration, expected_type=type_hints["chunking_configuration"])
            check_type(argname="argument parsing_configuration", value=parsing_configuration, expected_type=type_hints["parsing_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chunking_configuration is not None:
            self._values["chunking_configuration"] = chunking_configuration
        if parsing_configuration is not None:
            self._values["parsing_configuration"] = parsing_configuration

    @builtins.property
    def chunking_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration"]]]:
        '''chunking_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#chunking_configuration BedrockagentDataSource#chunking_configuration}
        '''
        result = self._values.get("chunking_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration"]]], result)

    @builtins.property
    def parsing_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration"]]]:
        '''parsing_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_configuration BedrockagentDataSource#parsing_configuration}
        '''
        result = self._values.get("parsing_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "chunking_strategy": "chunkingStrategy",
        "fixed_size_chunking_configuration": "fixedSizeChunkingConfiguration",
        "hierarchical_chunking_configuration": "hierarchicalChunkingConfiguration",
        "semantic_chunking_configuration": "semanticChunkingConfiguration",
    },
)
class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration:
    def __init__(
        self,
        *,
        chunking_strategy: builtins.str,
        fixed_size_chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hierarchical_chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        semantic_chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param chunking_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#chunking_strategy BedrockagentDataSource#chunking_strategy}.
        :param fixed_size_chunking_configuration: fixed_size_chunking_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#fixed_size_chunking_configuration BedrockagentDataSource#fixed_size_chunking_configuration}
        :param hierarchical_chunking_configuration: hierarchical_chunking_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#hierarchical_chunking_configuration BedrockagentDataSource#hierarchical_chunking_configuration}
        :param semantic_chunking_configuration: semantic_chunking_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#semantic_chunking_configuration BedrockagentDataSource#semantic_chunking_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea96a4cebb2e1d2cc38e3db1f2804fca90be3c8a1b64c36646932bde215d439)
            check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
            check_type(argname="argument fixed_size_chunking_configuration", value=fixed_size_chunking_configuration, expected_type=type_hints["fixed_size_chunking_configuration"])
            check_type(argname="argument hierarchical_chunking_configuration", value=hierarchical_chunking_configuration, expected_type=type_hints["hierarchical_chunking_configuration"])
            check_type(argname="argument semantic_chunking_configuration", value=semantic_chunking_configuration, expected_type=type_hints["semantic_chunking_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "chunking_strategy": chunking_strategy,
        }
        if fixed_size_chunking_configuration is not None:
            self._values["fixed_size_chunking_configuration"] = fixed_size_chunking_configuration
        if hierarchical_chunking_configuration is not None:
            self._values["hierarchical_chunking_configuration"] = hierarchical_chunking_configuration
        if semantic_chunking_configuration is not None:
            self._values["semantic_chunking_configuration"] = semantic_chunking_configuration

    @builtins.property
    def chunking_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#chunking_strategy BedrockagentDataSource#chunking_strategy}.'''
        result = self._values.get("chunking_strategy")
        assert result is not None, "Required property 'chunking_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fixed_size_chunking_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration"]]]:
        '''fixed_size_chunking_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#fixed_size_chunking_configuration BedrockagentDataSource#fixed_size_chunking_configuration}
        '''
        result = self._values.get("fixed_size_chunking_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration"]]], result)

    @builtins.property
    def hierarchical_chunking_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration"]]]:
        '''hierarchical_chunking_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#hierarchical_chunking_configuration BedrockagentDataSource#hierarchical_chunking_configuration}
        '''
        result = self._values.get("hierarchical_chunking_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration"]]], result)

    @builtins.property
    def semantic_chunking_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration"]]]:
        '''semantic_chunking_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#semantic_chunking_configuration BedrockagentDataSource#semantic_chunking_configuration}
        '''
        result = self._values.get("semantic_chunking_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "max_tokens": "maxTokens",
        "overlap_percentage": "overlapPercentage",
    },
)
class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration:
    def __init__(
        self,
        *,
        max_tokens: jsii.Number,
        overlap_percentage: jsii.Number,
    ) -> None:
        '''
        :param max_tokens: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#max_tokens BedrockagentDataSource#max_tokens}.
        :param overlap_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#overlap_percentage BedrockagentDataSource#overlap_percentage}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a5e9d0e220444c2ddc0a5c8383011bf4cdf5d1e00828dabb71147da58e2d7a)
            check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
            check_type(argname="argument overlap_percentage", value=overlap_percentage, expected_type=type_hints["overlap_percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_tokens": max_tokens,
            "overlap_percentage": overlap_percentage,
        }

    @builtins.property
    def max_tokens(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#max_tokens BedrockagentDataSource#max_tokens}.'''
        result = self._values.get("max_tokens")
        assert result is not None, "Required property 'max_tokens' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def overlap_percentage(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#overlap_percentage BedrockagentDataSource#overlap_percentage}.'''
        result = self._values.get("overlap_percentage")
        assert result is not None, "Required property 'overlap_percentage' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b513a0d2a148624b2246bdbf079a247737fb4333a0cbe7f734f248d2cd75e41b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b5d7a58b9cccc57986ef886c456bba4fff683a39c7c6533af024648ba44835)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1b9ac9e5ee609a7115eeca3719a3615954a517c5e7649d37f281164c6265ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6981b9dd676ccdca5c2cb15a8022ece2dd7f85ee6bcffaba11113523f6dc6c38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a311246bc8c52790eafac3c07f6d222c00ac283b9bca00a3167268a2c069a4c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b806ab20af7f9fbbd6afdd74e12687d927a8a770ecb2637788035943f53cabc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0372bbe7aacb183708657cff7886058c092b5c78ff9d3034e1bd6c6d8bf6de5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxTokensInput")
    def max_tokens_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTokensInput"))

    @builtins.property
    @jsii.member(jsii_name="overlapPercentageInput")
    def overlap_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "overlapPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTokens")
    def max_tokens(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTokens"))

    @max_tokens.setter
    def max_tokens(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ddda48fea0f5f6f57461c4632db3fb512bb16e126b4a84ed2acfc01d7ae9d30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="overlapPercentage")
    def overlap_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "overlapPercentage"))

    @overlap_percentage.setter
    def overlap_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b8c452772f623b8aa23bcb8b2d6204eb9cdb5c3e44928ac0b3b68282c41c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overlapPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d45ee74a05209bf03e6bc27617a0e2b4b32977d4b7747f9e0d2cfdab58ebdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "overlap_tokens": "overlapTokens",
        "level_configuration": "levelConfiguration",
    },
)
class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration:
    def __init__(
        self,
        *,
        overlap_tokens: jsii.Number,
        level_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param overlap_tokens: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#overlap_tokens BedrockagentDataSource#overlap_tokens}.
        :param level_configuration: level_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#level_configuration BedrockagentDataSource#level_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f004f4882d5b7b6d3a81892adfcd8c755f7d853d210807f3f98e73d93f80b2fa)
            check_type(argname="argument overlap_tokens", value=overlap_tokens, expected_type=type_hints["overlap_tokens"])
            check_type(argname="argument level_configuration", value=level_configuration, expected_type=type_hints["level_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "overlap_tokens": overlap_tokens,
        }
        if level_configuration is not None:
            self._values["level_configuration"] = level_configuration

    @builtins.property
    def overlap_tokens(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#overlap_tokens BedrockagentDataSource#overlap_tokens}.'''
        result = self._values.get("overlap_tokens")
        assert result is not None, "Required property 'overlap_tokens' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def level_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration"]]]:
        '''level_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#level_configuration BedrockagentDataSource#level_configuration}
        '''
        result = self._values.get("level_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration",
    jsii_struct_bases=[],
    name_mapping={"max_tokens": "maxTokens"},
)
class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration:
    def __init__(self, *, max_tokens: jsii.Number) -> None:
        '''
        :param max_tokens: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#max_tokens BedrockagentDataSource#max_tokens}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284424e14f6c6958180a2062e85e8997fe3c564bf60a25ed30a028dcd86ab1bf)
            check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_tokens": max_tokens,
        }

    @builtins.property
    def max_tokens(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#max_tokens BedrockagentDataSource#max_tokens}.'''
        result = self._values.get("max_tokens")
        assert result is not None, "Required property 'max_tokens' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c6183f477f504e1a07d4a29c64b7e3c66610310ac7d7aa1a7472a46a399977d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0608b008c71196a72cdb6f923f90a8073bd1f2c75d729ed4ddd97b6166b6898)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5adf86e065bfe4d1deb4525e01e84b50a10f2c6d6a63080b1e74d218aaf4026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77dfe17017580525d46569599d9e4deffb48d465adfc02f8e07015557604eb6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9320b0289ecb7f83baf860ea8c2d5926577812d035ae9ddd430e379ab5bd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84bb8d7399e52fcd563d79ae70353a6cc9582b39bc7599815a3528a95454f99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5e9452611848cdc24d39cb57d5c0e3c4afd5806538680c18fd84d48e0ce83c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxTokensInput")
    def max_tokens_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTokensInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTokens")
    def max_tokens(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxTokens"))

    @max_tokens.setter
    def max_tokens(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce3cb660adb3c7d812b837e3fd761c58e7e4e22027ff156f23cff155d5fb54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3fe94b3e3ccbd90e2bd946228b70da7b237a2ee8531945db9568993ef3bd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fb31f22422719b56aed76552b92bfa851502c7390ea4fa7992f7024afd8862)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171e3950b96d6d1f3cde5185b34d471b19755275a668ec3af9183998c8590dd2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ade17e20827ff77d7ca508e74cb7e1e89398821ab1c9d2602f0a6ae7772ecf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f57433cb2b564279d5b01ba289b5a30702c5a78e4177a4d9e036b032b523a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dc21c73cdd68b133ea78ff5eee42e249cf12cd9fb4a587a5ecba34ab9ac4f23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b28380c622e7eaa1e7155c7872faa1af36ab5d03de8318eb3f5d2cfad1ef22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a655dff5bda758bad19f6410a320d2eaa37c2fb77f21affe35929eca12f37c54)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLevelConfiguration")
    def put_level_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b839d2afbd738de6f1d7010145cb6c4aea3032aa1bf95502a56b8e408d183dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLevelConfiguration", [value]))

    @jsii.member(jsii_name="resetLevelConfiguration")
    def reset_level_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevelConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="levelConfiguration")
    def level_configuration(
        self,
    ) -> BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationList:
        return typing.cast(BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationList, jsii.get(self, "levelConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="levelConfigurationInput")
    def level_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]], jsii.get(self, "levelConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="overlapTokensInput")
    def overlap_tokens_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "overlapTokensInput"))

    @builtins.property
    @jsii.member(jsii_name="overlapTokens")
    def overlap_tokens(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "overlapTokens"))

    @overlap_tokens.setter
    def overlap_tokens(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e561aa97d9be2ff0581808ce7695d8225ced298f0a9c080a84297ee3dd7ef3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overlapTokens", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17a70e3dad3827e6b270831ba57cb50ed8a1973df34567d231ccebe3a63c913)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df6f62ba291d820c5947c8ba8926d9b28d758f2df55badcac2030fb427082fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07defb5e9dcfb033db494584ad81625fdeb55a31cc3e9033ff489a4b958af000)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf099f0ea78f31666f8b2c3a48eae255d15c3d9be042023c421e087fa08c48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3908582163ec9a310f0c7f015495835797241f4f95acb007c170b3b4ffcb8d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc65b08d3b8211aeab0cd1ae9e09959e4241eb581a8a369e75fc5bd8609c4960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182925022c553520a9c361f4df8c3925a374a4a261257243914ef8faccdb60da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84a27a8bb3a8eddc59f91802cfb61c1a2b282f1a5c82ea058cba898eea87333)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFixedSizeChunkingConfiguration")
    def put_fixed_size_chunking_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d0250420e4b73ad2d1477c233589a88c92e45b74f952989f56a5823eb6830b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFixedSizeChunkingConfiguration", [value]))

    @jsii.member(jsii_name="putHierarchicalChunkingConfiguration")
    def put_hierarchical_chunking_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88181c65f317050183b0625038d4d26207de22a35e3a042587ad1dcd013100fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHierarchicalChunkingConfiguration", [value]))

    @jsii.member(jsii_name="putSemanticChunkingConfiguration")
    def put_semantic_chunking_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02c5adb6018c85a35ee0033cca8addeb1b5ecd110dfc4f55063bca9a38166cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSemanticChunkingConfiguration", [value]))

    @jsii.member(jsii_name="resetFixedSizeChunkingConfiguration")
    def reset_fixed_size_chunking_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedSizeChunkingConfiguration", []))

    @jsii.member(jsii_name="resetHierarchicalChunkingConfiguration")
    def reset_hierarchical_chunking_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHierarchicalChunkingConfiguration", []))

    @jsii.member(jsii_name="resetSemanticChunkingConfiguration")
    def reset_semantic_chunking_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSemanticChunkingConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="fixedSizeChunkingConfiguration")
    def fixed_size_chunking_configuration(
        self,
    ) -> BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationList:
        return typing.cast(BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationList, jsii.get(self, "fixedSizeChunkingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="hierarchicalChunkingConfiguration")
    def hierarchical_chunking_configuration(
        self,
    ) -> BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationList:
        return typing.cast(BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationList, jsii.get(self, "hierarchicalChunkingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="semanticChunkingConfiguration")
    def semantic_chunking_configuration(
        self,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationList":
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationList", jsii.get(self, "semanticChunkingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="chunkingStrategyInput")
    def chunking_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chunkingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedSizeChunkingConfigurationInput")
    def fixed_size_chunking_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]], jsii.get(self, "fixedSizeChunkingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="hierarchicalChunkingConfigurationInput")
    def hierarchical_chunking_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]], jsii.get(self, "hierarchicalChunkingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="semanticChunkingConfigurationInput")
    def semantic_chunking_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration"]]], jsii.get(self, "semanticChunkingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="chunkingStrategy")
    def chunking_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chunkingStrategy"))

    @chunking_strategy.setter
    def chunking_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48eb557cb933708e958482afe8df51b126f7b19896ced78c7fcfc0ed42348733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chunkingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62fed68b74f01845ecd9c9124c228fd389b061d51f8670f81ab85e97b685a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "breakpoint_percentile_threshold": "breakpointPercentileThreshold",
        "buffer_size": "bufferSize",
        "max_token": "maxToken",
    },
)
class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration:
    def __init__(
        self,
        *,
        breakpoint_percentile_threshold: jsii.Number,
        buffer_size: jsii.Number,
        max_token: jsii.Number,
    ) -> None:
        '''
        :param breakpoint_percentile_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#breakpoint_percentile_threshold BedrockagentDataSource#breakpoint_percentile_threshold}.
        :param buffer_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#buffer_size BedrockagentDataSource#buffer_size}.
        :param max_token: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#max_token BedrockagentDataSource#max_token}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d68bd3f369e02ca22735793b57593c014b4eda1076487437afa17f71204e0f2)
            check_type(argname="argument breakpoint_percentile_threshold", value=breakpoint_percentile_threshold, expected_type=type_hints["breakpoint_percentile_threshold"])
            check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
            check_type(argname="argument max_token", value=max_token, expected_type=type_hints["max_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "breakpoint_percentile_threshold": breakpoint_percentile_threshold,
            "buffer_size": buffer_size,
            "max_token": max_token,
        }

    @builtins.property
    def breakpoint_percentile_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#breakpoint_percentile_threshold BedrockagentDataSource#breakpoint_percentile_threshold}.'''
        result = self._values.get("breakpoint_percentile_threshold")
        assert result is not None, "Required property 'breakpoint_percentile_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def buffer_size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#buffer_size BedrockagentDataSource#buffer_size}.'''
        result = self._values.get("buffer_size")
        assert result is not None, "Required property 'buffer_size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_token(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#max_token BedrockagentDataSource#max_token}.'''
        result = self._values.get("max_token")
        assert result is not None, "Required property 'max_token' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633873d72856bc42cd9aae28345033886ad273f28b99864f085c59ba7644ab1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d1285c430b6b254209f1661a655d48b75fd3868ab5295773343fd1324bdecf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b0ad196b47a064ba16ca72d3a5d4087e12338c39b155f3a0e68d7647fd1981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17dba2c15def18d1332393134b6cb98dc1765604f8da148017cba838b0dbaecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa45a96180534c63cf505fa8319bbc25a02159cdbaf68c4abc5591e88105a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77956aaf7607b34ac3fef45b2a1203be891729b4efe0a4e98ca174362ddccff6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c82344a6aef5cbfe88a194988a84ef8b6d9c86fe9db4c462be76656e1d1f3a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="breakpointPercentileThresholdInput")
    def breakpoint_percentile_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "breakpointPercentileThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="bufferSizeInput")
    def buffer_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bufferSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxTokenInput")
    def max_token_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="breakpointPercentileThreshold")
    def breakpoint_percentile_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "breakpointPercentileThreshold"))

    @breakpoint_percentile_threshold.setter
    def breakpoint_percentile_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75d2c4c09a50ef976c609c2d390713d95826e106746c8f0ea75208f0d97382c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "breakpointPercentileThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bufferSize")
    def buffer_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bufferSize"))

    @buffer_size.setter
    def buffer_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c554dfd5b0cae7b167e5c0a44e3bc9ce1b9119e7c70128f9541df0046b5e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bufferSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxToken")
    def max_token(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxToken"))

    @max_token.setter
    def max_token(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd568ce5f2b4e61b73dabef94bf304c9a5ae6f41a47c9ff6ee6970eb79e9a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb9c00dfbe26a8faa3bfe6d6ad19ef430e6bf0224e5a55d2d4ddc532597ef27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec80dae3ebe7d7e80bfb178ca537b3b3964a6c5ac630d40124717e6c7784b70a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee07039a47955995a9b490d9b7b9f93a5d10687697c374bcaf6a176934fb7d79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858d4784285cde94cc96f7a2c86e0fefd8bb3596d198ec1433ffdd09aeba3391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6338925885a9cda3d3220bb7ccd47ac6e3f9128369111a0a1ea73fdf406c9ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce88b4d13d98998f786946237bb89d17a4a8a3d9adc39ab005a84fff0b40874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d7d4869d7ca45888f1eae7ff765222fda87628b3246e61c33ed21bb961d0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2543d1164e0949c6d96aeeb5a49b571590038661c566e1e428b120f7cb211cbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putChunkingConfiguration")
    def put_chunking_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a0accb99ea65607544018f4a664d6bfa615bcf2b689b6a66a793b6fab33264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putChunkingConfiguration", [value]))

    @jsii.member(jsii_name="putParsingConfiguration")
    def put_parsing_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a9dd6d34e14b9d3b5ce86661e472ab137cf9d76e7a481c944e24102cbce5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParsingConfiguration", [value]))

    @jsii.member(jsii_name="resetChunkingConfiguration")
    def reset_chunking_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChunkingConfiguration", []))

    @jsii.member(jsii_name="resetParsingConfiguration")
    def reset_parsing_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParsingConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="chunkingConfiguration")
    def chunking_configuration(
        self,
    ) -> BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationList:
        return typing.cast(BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationList, jsii.get(self, "chunkingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="parsingConfiguration")
    def parsing_configuration(
        self,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationList":
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationList", jsii.get(self, "parsingConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="chunkingConfigurationInput")
    def chunking_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]], jsii.get(self, "chunkingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingConfigurationInput")
    def parsing_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration"]]], jsii.get(self, "parsingConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae33bb9bc9d4a43ae9cc644466ac45aabc9376c796fe67716c87cd6513ca5e9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "parsing_strategy": "parsingStrategy",
        "bedrock_foundation_model_configuration": "bedrockFoundationModelConfiguration",
    },
)
class BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration:
    def __init__(
        self,
        *,
        parsing_strategy: builtins.str,
        bedrock_foundation_model_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param parsing_strategy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_strategy BedrockagentDataSource#parsing_strategy}.
        :param bedrock_foundation_model_configuration: bedrock_foundation_model_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#bedrock_foundation_model_configuration BedrockagentDataSource#bedrock_foundation_model_configuration}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55d158134b7cba55844ba9bb0c8d22cad81e740128a9ee01976a12825a34a6a)
            check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            check_type(argname="argument bedrock_foundation_model_configuration", value=bedrock_foundation_model_configuration, expected_type=type_hints["bedrock_foundation_model_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parsing_strategy": parsing_strategy,
        }
        if bedrock_foundation_model_configuration is not None:
            self._values["bedrock_foundation_model_configuration"] = bedrock_foundation_model_configuration

    @builtins.property
    def parsing_strategy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_strategy BedrockagentDataSource#parsing_strategy}.'''
        result = self._values.get("parsing_strategy")
        assert result is not None, "Required property 'parsing_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bedrock_foundation_model_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration"]]]:
        '''bedrock_foundation_model_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#bedrock_foundation_model_configuration BedrockagentDataSource#bedrock_foundation_model_configuration}
        '''
        result = self._values.get("bedrock_foundation_model_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration",
    jsii_struct_bases=[],
    name_mapping={"model_arn": "modelArn", "parsing_prompt": "parsingPrompt"},
)
class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration:
    def __init__(
        self,
        *,
        model_arn: builtins.str,
        parsing_prompt: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param model_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#model_arn BedrockagentDataSource#model_arn}.
        :param parsing_prompt: parsing_prompt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_prompt BedrockagentDataSource#parsing_prompt}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2f98d98f166dc6646598d51289e45537f569dc0e373abf28503edf76c439f0)
            check_type(argname="argument model_arn", value=model_arn, expected_type=type_hints["model_arn"])
            check_type(argname="argument parsing_prompt", value=parsing_prompt, expected_type=type_hints["parsing_prompt"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "model_arn": model_arn,
        }
        if parsing_prompt is not None:
            self._values["parsing_prompt"] = parsing_prompt

    @builtins.property
    def model_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#model_arn BedrockagentDataSource#model_arn}.'''
        result = self._values.get("model_arn")
        assert result is not None, "Required property 'model_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parsing_prompt(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt"]]]:
        '''parsing_prompt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_prompt BedrockagentDataSource#parsing_prompt}
        '''
        result = self._values.get("parsing_prompt")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f627043eff7fa5fbeef2d1259a7f23cd5cfd9c4966c4d312b216ae48cf73fcb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3ce5972a4389d8d9f587aef6fa7fde118ef5c7be0d4cc7be0091dc3bca2720)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec32ca42601cfa70ea4bd8ee57086531b75f80e0153e6a23c6a5c26b6cb28915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c473e8a9a57c242bda8df8a1d47ae0a17e7c2b6bcbd9a5110b3874fa84b4fab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95df0714350b8808afeeb07e55e77abed3725c6b0961c201a7d6c0975392988b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36faf76a0b38d01e42c27ad0c6edef415c428afbbc1d6c19e4292bbbab4273e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4635cf93151f71640fc7206ed7e9f6db35593618877d9db170fb94c482f816d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParsingPrompt")
    def put_parsing_prompt(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b59f790480deeb2f998e71d88290de4a798751e8fa89c77ab000a23849dd36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParsingPrompt", [value]))

    @jsii.member(jsii_name="resetParsingPrompt")
    def reset_parsing_prompt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParsingPrompt", []))

    @builtins.property
    @jsii.member(jsii_name="parsingPrompt")
    def parsing_prompt(
        self,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptList":
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptList", jsii.get(self, "parsingPrompt"))

    @builtins.property
    @jsii.member(jsii_name="modelArnInput")
    def model_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelArnInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingPromptInput")
    def parsing_prompt_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt"]]], jsii.get(self, "parsingPromptInput"))

    @builtins.property
    @jsii.member(jsii_name="modelArn")
    def model_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelArn"))

    @model_arn.setter
    def model_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397b33edcda39fd3414400f34477867e076770638425b3d006cccc430f88575e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0a6ebc6c4d80c6ebaea054c9f9ebe16ef1e3eccdd594391d0c3c3157e1990b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt",
    jsii_struct_bases=[],
    name_mapping={"parsing_prompt_string": "parsingPromptString"},
)
class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt:
    def __init__(self, *, parsing_prompt_string: builtins.str) -> None:
        '''
        :param parsing_prompt_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_prompt_string BedrockagentDataSource#parsing_prompt_string}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2129d8acac6cad7e65377af3e685427d7087efa617ebe734bb0c5c350b37ffb2)
            check_type(argname="argument parsing_prompt_string", value=parsing_prompt_string, expected_type=type_hints["parsing_prompt_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "parsing_prompt_string": parsing_prompt_string,
        }

    @builtins.property
    def parsing_prompt_string(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.69.0/docs/resources/bedrockagent_data_source#parsing_prompt_string BedrockagentDataSource#parsing_prompt_string}.'''
        result = self._values.get("parsing_prompt_string")
        assert result is not None, "Required property 'parsing_prompt_string' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0e6e613871a8290eb6d04a77dfb168d1b5506059c9f080ccc51383cfc31dcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc0e17a16d7dd6290e48b38b503fc9e1a5eac46f02541972cb65f0f509fbf6aa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699db1cf3527300dce4b85afdf351679a91487e62c98038168b76f0144010431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b23fac81d3ef49087f5263ceb5ae21e360cfc11e6e44dfc38b57db996c52bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48849fb5e163bd4bedaee9beffa46803ce12dab8a417bb0e183316de408bd8d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26329335131340e793eac6d9e7a79c0c74775982ec4d35c0b5cfe23fddaea43c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3471399d27b2d636406e05f1686192e17d1c930057afdf46fc55d33b6c520c7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="parsingPromptStringInput")
    def parsing_prompt_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parsingPromptStringInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingPromptString")
    def parsing_prompt_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parsingPromptString"))

    @parsing_prompt_string.setter
    def parsing_prompt_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8417452896a85824aa9d452a7d1025e2ed7ce1cf0e263d08debfab7ecb8e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parsingPromptString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041e44842a1f420a8ae2918a50a9d58d77f6c6dc0d5ff64652a2e9025ba87588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c585b427abaef05de9a62ac3607dd3996394eb24bfbdd8ac7e7147b70d951e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b040779a945a30bde607b226e9401845640b448de151bb1e8c94ff68cfcf5db)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0e3e04674e682d065c82abf87aef23982d0688384df7b7549b33bd88532930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fa8cbf5d3c24f9f5d60c46aac9d2cc86fc468722e139ca11f80e4e386e2f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309dbea3ad5be0f180b8b21700c77dbed95a8b30af5ee7928508c4fe9ee5e52c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ccd2b0037f65d3f1063cd55fe226ed091b463c7efbf90d3764a03c86bbf094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.bedrockagentDataSource.BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a01f336744191e13de648d7def5c3bc8ef0594e17c736cd02029f50a210ff6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBedrockFoundationModelConfiguration")
    def put_bedrock_foundation_model_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed79e58553ddd6dc2d5c76ff77c9c386d8be1864e5851f9ba7c11b95d1efd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBedrockFoundationModelConfiguration", [value]))

    @jsii.member(jsii_name="resetBedrockFoundationModelConfiguration")
    def reset_bedrock_foundation_model_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBedrockFoundationModelConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="bedrockFoundationModelConfiguration")
    def bedrock_foundation_model_configuration(
        self,
    ) -> BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationList:
        return typing.cast(BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationList, jsii.get(self, "bedrockFoundationModelConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="bedrockFoundationModelConfigurationInput")
    def bedrock_foundation_model_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]], jsii.get(self, "bedrockFoundationModelConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingStrategyInput")
    def parsing_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parsingStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="parsingStrategy")
    def parsing_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parsingStrategy"))

    @parsing_strategy.setter
    def parsing_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4da69e5750894d108af89f4932e202c08b6196f7755dd28e767ca793a1a8531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parsingStrategy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f4f7b934c24f65562174e0616eb84100a26599c77f47f46f4454a9b110502d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BedrockagentDataSource",
    "BedrockagentDataSourceConfig",
    "BedrockagentDataSourceDataSourceConfiguration",
    "BedrockagentDataSourceDataSourceConfigurationList",
    "BedrockagentDataSourceDataSourceConfigurationOutputReference",
    "BedrockagentDataSourceDataSourceConfigurationS3Configuration",
    "BedrockagentDataSourceDataSourceConfigurationS3ConfigurationList",
    "BedrockagentDataSourceDataSourceConfigurationS3ConfigurationOutputReference",
    "BedrockagentDataSourceServerSideEncryptionConfiguration",
    "BedrockagentDataSourceServerSideEncryptionConfigurationList",
    "BedrockagentDataSourceServerSideEncryptionConfigurationOutputReference",
    "BedrockagentDataSourceTimeouts",
    "BedrockagentDataSourceTimeoutsOutputReference",
    "BedrockagentDataSourceVectorIngestionConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptList",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPromptOutputReference",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationList",
    "BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__499da3284ad1f3481c99bcbd79758f3c78e47f604b996226e6bff6cb2641b0f6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    knowledge_base_id: builtins.str,
    name: builtins.str,
    data_deletion_policy: typing.Optional[builtins.str] = None,
    data_source_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[BedrockagentDataSourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vector_ingestion_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7280012840639152b759fa042c3572c225b8865b2eff7f3224af16ca056f2885(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19560266da7143f13dd4aa6febbb9a386282a3bbdfbe6a1fbe39fd3dc1b19045(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14839d87ddf30e9a12b452cb7d6147d893edc8e21ea8bf5106476bb37e40c1e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8ed8a2df48e466b68173a80d202d12924c7a7d2ec880c42025feed292993a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da415da3b18aa16a19a9aa00c4bf6c2640680f1b35b4bda8bbc87f5da846949(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c789628668987a09cdda7ef7a0656bda6a8005e73b69ee384b10513e761d4a70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af829b6389ff95731ad16302f79d827c0909f6a83b0619d74f4b178763f091eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f12b586bc5fd427d7b3114bec93476ffa3a9509c703b843e40ea06c1badbe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2df85ee439b62a35399d661f3574eb62b06cc43b81ec6d3247dfd59fdf447cc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    knowledge_base_id: builtins.str,
    name: builtins.str,
    data_deletion_policy: typing.Optional[builtins.str] = None,
    data_source_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceDataSourceConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceServerSideEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[BedrockagentDataSourceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vector_ingestion_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a53260b5eda595cd7f287dee58d19e5f2e1e38f3db9b35078991b4886a91a2f(
    *,
    type: builtins.str,
    s3_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceDataSourceConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83723fe6725bc85d420b5f41e422b123738dadea0d0d2908e91cd03417eb9050(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8385c422e57ab149b420f48407873e1706bb42d11e3169b7ed1e321f2694fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac55f4df787f679c9994ce232dde4b8bfe8f860a2b81a0a5f98ea804e79f1a0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0247ffecb90087ec4345189e7557500c62798b12acce2cd723a7414261a22823(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1193f6eedd1640c22441459499178b0072e4077f27e9e05ae5e521698479ab9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08381c1cb3f696e4aed39440c481379aaf132fa31005dfecff03fca02fef72b0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3962d119ad0eb7585fd5cda968c6c1741b3a18c5940fd2bd03110a2169cb7dbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d0d0342c5ba48607d21fd2e721f6303ffe75bd2c290a1dffadf0b86a8315bf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceDataSourceConfigurationS3Configuration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e45f76bcf902a0defd3f603e1e44e2dcd6a05d9e54c4c38786ea0b82e89ad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7feebe0d4712b7020dc65dc6f236afe601987996bd45c47dbfc690c6df92ae1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be09d318ee91b8038bed7ab3191c81f1fea450260e388b6bafbe34322372404(
    *,
    bucket_arn: builtins.str,
    bucket_owner_account_id: typing.Optional[builtins.str] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b3c650dbb69943787a9277964cf71e7e7a93ce336b41607b428f6a50a10eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807a84d3edbf75f4586c76cce7ffe5bf36983fe67e71a811e0f0a480fcbccbed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf39eb595202cef18d9027dc0154823313754fcf927cfee5b83b2eeeebf7c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f822415f0aa218717f05372f2490f1dc887695c1842b9d9704240b905ad20f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83b49a69f07684cd41ac4868f56ba4233bd2acf0146b9e12cb5727ef9e31f19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b429364b0aa9acec05982b8cf28153ecb2739a5f6dd06c10760f6180775735(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceDataSourceConfigurationS3Configuration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504950f1cea4c5646870b528191304d02a78929b3499303888989a00bbf03c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c28c449efef35027d18857f6b4db5c746b901645027927cdfa9f8a9161c653(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e963405ee51a96cba8f4cc2e38882876108f9e3dc13c12f5a13f4e92ea31ec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc1061ebc3c9102e46617eeeb34df6f89c7c970cde7b99ab4cc7501cc938cd5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7a501f33f9b294efe6c0df37f648773408461db7932e45baba80aa6b2c2a79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceDataSourceConfigurationS3Configuration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86df8e9c1018ef4b06b6422efcc721c56db31415cf4af17bfc256968a7c02cd4(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8dfaa8af5aaef2a77b465459a284eff91658b2e8e9ba9bae1f857de3d8221f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de23e9714ff0a2453fbfb621dcc4187b4b30dd0923dd75e7d024cac29d6a00d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1d53f3bd5837d7de666ebfbf2e1c497ab869817eee4ee4ce453ffe8ce2aaad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d4e8f93bea1f9a9fb8bd95338131a2c10d4bccb2b793eff178c845ad7d9602(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b571bb3093705db7474b25967298c24acf2235766c8036bbc294930ed4ea484d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aed545102bcb68ffc55298aefdce7d5e20cdbee33192b78ffc33bc8dfb6d8a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceServerSideEncryptionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f492837cd84eff243ff6a6a75727880e829eb39318675e487bc01d6cec1e6812(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d145fa975730aff6b1e161a5aa6b4b5ee331e451277f914793d8a6c53156d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42aa785c624c26bade26f03e536aab991652ea52c60f53fc6ee5696045c6ad93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceServerSideEncryptionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da42f6a13d38feeef76a411967f6705b91883dba3dd8a12b073c8906956acf1c(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567fca939951ec876941ce6cafe11d30d3c6933ecb29d1d8f59def92f67a4870(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f2ee45214c3a22b1a2fb4241be52b7452c8760ff015522172b0f9f65401ae2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdb5e4ce5de8289e4fe2652ee891c0689f01a2cb600d2698ec12819a8a33a82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2ae89fc74d7d919227d3812c37215c6d81a4c4c5d6e99d0ee506f16ba500a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70149422f201a4edffcb7a4a9b980760573b6faf9dee871ed67b58e3fe90935c(
    *,
    chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parsing_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea96a4cebb2e1d2cc38e3db1f2804fca90be3c8a1b64c36646932bde215d439(
    *,
    chunking_strategy: builtins.str,
    fixed_size_chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hierarchical_chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    semantic_chunking_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a5e9d0e220444c2ddc0a5c8383011bf4cdf5d1e00828dabb71147da58e2d7a(
    *,
    max_tokens: jsii.Number,
    overlap_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b513a0d2a148624b2246bdbf079a247737fb4333a0cbe7f734f248d2cd75e41b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b5d7a58b9cccc57986ef886c456bba4fff683a39c7c6533af024648ba44835(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1b9ac9e5ee609a7115eeca3719a3615954a517c5e7649d37f281164c6265ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6981b9dd676ccdca5c2cb15a8022ece2dd7f85ee6bcffaba11113523f6dc6c38(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a311246bc8c52790eafac3c07f6d222c00ac283b9bca00a3167268a2c069a4c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b806ab20af7f9fbbd6afdd74e12687d927a8a770ecb2637788035943f53cabc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0372bbe7aacb183708657cff7886058c092b5c78ff9d3034e1bd6c6d8bf6de5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ddda48fea0f5f6f57461c4632db3fb512bb16e126b4a84ed2acfc01d7ae9d30(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b8c452772f623b8aa23bcb8b2d6204eb9cdb5c3e44928ac0b3b68282c41c94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d45ee74a05209bf03e6bc27617a0e2b4b32977d4b7747f9e0d2cfdab58ebdc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f004f4882d5b7b6d3a81892adfcd8c755f7d853d210807f3f98e73d93f80b2fa(
    *,
    overlap_tokens: jsii.Number,
    level_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284424e14f6c6958180a2062e85e8997fe3c564bf60a25ed30a028dcd86ab1bf(
    *,
    max_tokens: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6183f477f504e1a07d4a29c64b7e3c66610310ac7d7aa1a7472a46a399977d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0608b008c71196a72cdb6f923f90a8073bd1f2c75d729ed4ddd97b6166b6898(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5adf86e065bfe4d1deb4525e01e84b50a10f2c6d6a63080b1e74d218aaf4026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dfe17017580525d46569599d9e4deffb48d465adfc02f8e07015557604eb6c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9320b0289ecb7f83baf860ea8c2d5926577812d035ae9ddd430e379ab5bd0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bb8d7399e52fcd563d79ae70353a6cc9582b39bc7599815a3528a95454f99b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5e9452611848cdc24d39cb57d5c0e3c4afd5806538680c18fd84d48e0ce83c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce3cb660adb3c7d812b837e3fd761c58e7e4e22027ff156f23cff155d5fb54b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3fe94b3e3ccbd90e2bd946228b70da7b237a2ee8531945db9568993ef3bd95(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fb31f22422719b56aed76552b92bfa851502c7390ea4fa7992f7024afd8862(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171e3950b96d6d1f3cde5185b34d471b19755275a668ec3af9183998c8590dd2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ade17e20827ff77d7ca508e74cb7e1e89398821ab1c9d2602f0a6ae7772ecf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f57433cb2b564279d5b01ba289b5a30702c5a78e4177a4d9e036b032b523a25(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc21c73cdd68b133ea78ff5eee42e249cf12cd9fb4a587a5ecba34ab9ac4f23(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b28380c622e7eaa1e7155c7872faa1af36ab5d03de8318eb3f5d2cfad1ef22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a655dff5bda758bad19f6410a320d2eaa37c2fb77f21affe35929eca12f37c54(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b839d2afbd738de6f1d7010145cb6c4aea3032aa1bf95502a56b8e408d183dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfigurationLevelConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e561aa97d9be2ff0581808ce7695d8225ced298f0a9c080a84297ee3dd7ef3c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17a70e3dad3827e6b270831ba57cb50ed8a1973df34567d231ccebe3a63c913(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df6f62ba291d820c5947c8ba8926d9b28d758f2df55badcac2030fb427082fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07defb5e9dcfb033db494584ad81625fdeb55a31cc3e9033ff489a4b958af000(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf099f0ea78f31666f8b2c3a48eae255d15c3d9be042023c421e087fa08c48a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3908582163ec9a310f0c7f015495835797241f4f95acb007c170b3b4ffcb8d22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc65b08d3b8211aeab0cd1ae9e09959e4241eb581a8a369e75fc5bd8609c4960(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182925022c553520a9c361f4df8c3925a374a4a261257243914ef8faccdb60da(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84a27a8bb3a8eddc59f91802cfb61c1a2b282f1a5c82ea058cba898eea87333(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0250420e4b73ad2d1477c233589a88c92e45b74f952989f56a5823eb6830b6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationFixedSizeChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88181c65f317050183b0625038d4d26207de22a35e3a042587ad1dcd013100fb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationHierarchicalChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02c5adb6018c85a35ee0033cca8addeb1b5ecd110dfc4f55063bca9a38166cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48eb557cb933708e958482afe8df51b126f7b19896ced78c7fcfc0ed42348733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62fed68b74f01845ecd9c9124c228fd389b061d51f8670f81ab85e97b685a50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d68bd3f369e02ca22735793b57593c014b4eda1076487437afa17f71204e0f2(
    *,
    breakpoint_percentile_threshold: jsii.Number,
    buffer_size: jsii.Number,
    max_token: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633873d72856bc42cd9aae28345033886ad273f28b99864f085c59ba7644ab1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d1285c430b6b254209f1661a655d48b75fd3868ab5295773343fd1324bdecf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b0ad196b47a064ba16ca72d3a5d4087e12338c39b155f3a0e68d7647fd1981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17dba2c15def18d1332393134b6cb98dc1765604f8da148017cba838b0dbaecb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa45a96180534c63cf505fa8319bbc25a02159cdbaf68c4abc5591e88105a6b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77956aaf7607b34ac3fef45b2a1203be891729b4efe0a4e98ca174362ddccff6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c82344a6aef5cbfe88a194988a84ef8b6d9c86fe9db4c462be76656e1d1f3a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75d2c4c09a50ef976c609c2d390713d95826e106746c8f0ea75208f0d97382c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c554dfd5b0cae7b167e5c0a44e3bc9ce1b9119e7c70128f9541df0046b5e69(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd568ce5f2b4e61b73dabef94bf304c9a5ae6f41a47c9ff6ee6970eb79e9a9e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb9c00dfbe26a8faa3bfe6d6ad19ef430e6bf0224e5a55d2d4ddc532597ef27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationChunkingConfigurationSemanticChunkingConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec80dae3ebe7d7e80bfb178ca537b3b3964a6c5ac630d40124717e6c7784b70a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee07039a47955995a9b490d9b7b9f93a5d10687697c374bcaf6a176934fb7d79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858d4784285cde94cc96f7a2c86e0fefd8bb3596d198ec1433ffdd09aeba3391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6338925885a9cda3d3220bb7ccd47ac6e3f9128369111a0a1ea73fdf406c9ffd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce88b4d13d98998f786946237bb89d17a4a8a3d9adc39ab005a84fff0b40874(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d7d4869d7ca45888f1eae7ff765222fda87628b3246e61c33ed21bb961d0e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2543d1164e0949c6d96aeeb5a49b571590038661c566e1e428b120f7cb211cbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a0accb99ea65607544018f4a664d6bfa615bcf2b689b6a66a793b6fab33264(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationChunkingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a9dd6d34e14b9d3b5ce86661e472ab137cf9d76e7a481c944e24102cbce5f8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae33bb9bc9d4a43ae9cc644466ac45aabc9376c796fe67716c87cd6513ca5e9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55d158134b7cba55844ba9bb0c8d22cad81e740128a9ee01976a12825a34a6a(
    *,
    parsing_strategy: builtins.str,
    bedrock_foundation_model_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2f98d98f166dc6646598d51289e45537f569dc0e373abf28503edf76c439f0(
    *,
    model_arn: builtins.str,
    parsing_prompt: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f627043eff7fa5fbeef2d1259a7f23cd5cfd9c4966c4d312b216ae48cf73fcb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3ce5972a4389d8d9f587aef6fa7fde118ef5c7be0d4cc7be0091dc3bca2720(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec32ca42601cfa70ea4bd8ee57086531b75f80e0153e6a23c6a5c26b6cb28915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c473e8a9a57c242bda8df8a1d47ae0a17e7c2b6bcbd9a5110b3874fa84b4fab2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95df0714350b8808afeeb07e55e77abed3725c6b0961c201a7d6c0975392988b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36faf76a0b38d01e42c27ad0c6edef415c428afbbc1d6c19e4292bbbab4273e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4635cf93151f71640fc7206ed7e9f6db35593618877d9db170fb94c482f816d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b59f790480deeb2f998e71d88290de4a798751e8fa89c77ab000a23849dd36(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397b33edcda39fd3414400f34477867e076770638425b3d006cccc430f88575e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0a6ebc6c4d80c6ebaea054c9f9ebe16ef1e3eccdd594391d0c3c3157e1990b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2129d8acac6cad7e65377af3e685427d7087efa617ebe734bb0c5c350b37ffb2(
    *,
    parsing_prompt_string: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0e6e613871a8290eb6d04a77dfb168d1b5506059c9f080ccc51383cfc31dcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0e17a16d7dd6290e48b38b503fc9e1a5eac46f02541972cb65f0f509fbf6aa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699db1cf3527300dce4b85afdf351679a91487e62c98038168b76f0144010431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b23fac81d3ef49087f5263ceb5ae21e360cfc11e6e44dfc38b57db996c52bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48849fb5e163bd4bedaee9beffa46803ce12dab8a417bb0e183316de408bd8d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26329335131340e793eac6d9e7a79c0c74775982ec4d35c0b5cfe23fddaea43c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3471399d27b2d636406e05f1686192e17d1c930057afdf46fc55d33b6c520c7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8417452896a85824aa9d452a7d1025e2ed7ce1cf0e263d08debfab7ecb8e67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041e44842a1f420a8ae2918a50a9d58d77f6c6dc0d5ff64652a2e9025ba87588(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfigurationParsingPrompt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c585b427abaef05de9a62ac3607dd3996394eb24bfbdd8ac7e7147b70d951e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b040779a945a30bde607b226e9401845640b448de151bb1e8c94ff68cfcf5db(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0e3e04674e682d065c82abf87aef23982d0688384df7b7549b33bd88532930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fa8cbf5d3c24f9f5d60c46aac9d2cc86fc468722e139ca11f80e4e386e2f7b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309dbea3ad5be0f180b8b21700c77dbed95a8b30af5ee7928508c4fe9ee5e52c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ccd2b0037f65d3f1063cd55fe226ed091b463c7efbf90d3764a03c86bbf094(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a01f336744191e13de648d7def5c3bc8ef0594e17c736cd02029f50a210ff6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed79e58553ddd6dc2d5c76ff77c9c386d8be1864e5851f9ba7c11b95d1efd43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BedrockagentDataSourceVectorIngestionConfigurationParsingConfigurationBedrockFoundationModelConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4da69e5750894d108af89f4932e202c08b6196f7755dd28e767ca793a1a8531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f4f7b934c24f65562174e0616eb84100a26599c77f47f46f4454a9b110502d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BedrockagentDataSourceVectorIngestionConfigurationParsingConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
